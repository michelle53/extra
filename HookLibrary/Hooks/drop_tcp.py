from scapy.all import * 

def run(packet):
    try:
        if packet.haslayer(TCP):
            return "Drop"
    except:
        raise "Error"
        
    return "Modification"
