from scapy.all import *
# Main Author/Resource : tintinweb@oststrom.com <github.com/tintinweb>



class TCP_Receiver(object):
    def start(self):
        return self.send_syn()

    def match_packet(self, pkt):
        if pkt.haslayer(IP) and pkt[IP].dst == self.l4[IP].src \
           and pkt.haslayer(TCP) and pkt[TCP].dport == self.sport \
           and pkt[TCP].ack == self.seq_next:
           return True
        return False

    def _sr1(self, pkt):
        send(pkt)
        ans = sniff(filter="tcp port %s"%self.target[1],lfilter=self.match_packet,count=1,timeout=1)
        return ans[0] if ans else None

    def handle_recv(self, pkt):
        if pkt and pkt.haslayer(IP) and pkt.haslayer(TCP):
            if pkt[TCP].flags & 0x3f == 0x12:   # SYN+ACK
                return self.send_synack_ack(pkt)
            elif  pkt[TCP].flags & 4 != 0:      # RST
                raise Exception("RST")
            elif pkt[TCP].flags & 0x1 == 1:     # FIN
                return self.send_finack(pkt)
            elif pkt[TCP].flags & 0x3f == 0x10: # FIN+ACK
                return self.send_ack(pkt)
        return None

    def send_syn(self):
        self.l4[TCP].flags = "S"
        self.seq_next = self.l4[TCP].seq + 1
        response = self._sr1(self.l4)
        self.l4[TCP].seq += 1
        return self.handle_recv(response)

    def send_synack_ack(self, pkt):
        self.l4[TCP].ack = pkt[TCP].seq+1
        self.l4[TCP].flags = "A"
        self.seq_next = self.l4[TCP].seq
        response = self._sr1(self.l4)
        return self.handle_recv(response)

    def send_data(self, d):
        self.l4[TCP].flags = "PA"
        response = self._sr1(self.l4/d)
        self.seq_next = self.l4[TCP].seq + len(d)
        self.l4[TCP].seq += len(d)
        return self.handle_recv(response)

    def send_fin(self):
        self.l4[TCP].flags = "F"
        self.seq_next = self.l4[TCP].seq + 1
        response = self._sr1(self.l4)
        self.l4[TCP].seq += 1
        return self.handle_recv(response)

    def send_finack(self, pkt):
        self.l4[TCP].flags = "FA"
        self.l4[TCP].ack = pkt[TCP].seq+1
        self.seq_next = self.l4[TCP].seq + 1
        response = send(self.l4)
        self.l4[TCP].seq += 1
        raise Exception("FIN+ACK")

    def send_ack(self, pkt):
        self.l4[TCP].flags = "A"
        self.l4[TCP].ack = pkt[TCP].seq+1
        self.seq_next = self.l4[TCP].seq + 1
        response = self._sr1(self.l4)
        self.l4[TCP].seq += 1
