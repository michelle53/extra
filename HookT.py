from scapy.all import *
from Hooks import change_tcp_port 
from Hooks import drop_tcp

packets = rdpcap('Mcap3.pcap')
packets2 = rdpcap('Mcap3.pcap')

def change_tcp_port_tester():
    for packet in packets:
        if packet.haslayer(TCP):
            print(packet[TCP].sport)
            change_tcp_port.run(packet)
            print(packet[TCP].sport)
            print("//")
# drop if the tcp contains a 
def drop_tcp_tester():
    print(len(packets2))
    for packet in packets2:
        if drop_tcp.run(packet) == "Drop":
            packets2.remove(packet)
    print(len(packets2))

if __name__== '__main__':
   # change_tcp_port_tester()
    drop_tcp_tester()


