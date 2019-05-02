from scapy.all import * 

def run(packet):
    try:
        if packet.haslayer(TCP):
            del packet.chksum
            del packet.getlayer(TCP).chksum
            packet.getlayer(TCP).src = 55555
    except:
        raise
    
    packet.show2(dump=True)
    return "Modification"

        
