from scapy.all import *
# Main Author/Resource : tintinweb@oststrom.com <github.com/tintinweb>



class TCP_Sender(object):
    def start(self, target):
        self.seq = 0
        self.seq_next = 0
        self.target = target
        self.dst = next(iter(Net(target[0])))
        self.dport = target[1]
        self.sport = random.randrange(0,2**16)
        self.l4 = IP(dst=target[0])/TCP(sport=self.sport, dport=self.dport, flags=0,
                                        seq=random.randrange(0,2**32))
        self.src = self.l4.src
        self.swin = self.l4[TCP].window
        self.dwin=1
        self.l4[TCP].flags = "S"
        self.seq_next = self.l4[TCP].seq + 1
        send(self.l4)
        self.l4[TCP].seq += 1       

   



