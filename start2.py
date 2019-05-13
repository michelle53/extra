from TCP_Receiver2 import TCP_Receiver
from TCP_Sender import TCP_Sender
import random

snd = TCP_Sender()
rc = TCP_Receiver()

#rc.start()
# for i in range(20):
#     snd.start("127.0.0.1")

from scapy.all import *

sport = random.randint(1024,65535)

# SYN
ip=IP(src='127.0.0.1',dst='127.0.0.1')
SYN=TCP(sport=sport,dport=443,flags='S',seq=1000)
SYNACK=sr1(ip/SYN)

# SYN-ACK
ACK=TCP(sport=sport, dport=443, flags='A', seq=SYNACK.ack + 1, ack=SYNACK.seq + 1)
send(ip/ACK)