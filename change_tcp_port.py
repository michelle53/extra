from scapy.all import * 

def run(packet):
    try:
        if packet.haslayer(TCP):
            del packet.chksum
            del packet.getlayer(TCP).chksum
            packet[TCP].sport = 55555
    except:
        raise
    #packet.show2(dump=True)

        
