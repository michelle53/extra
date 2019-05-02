from scapy.all import * 

def run(packet):
    try:
        if packet.haslayer(DNS):
            del packet.chksum
            del packet.getlayer(DNS).chksum
            packet.getlayer(DNS).src = 44444
    except:
        raise
    
    packet.show2(dump=True)
    return "Modification"
