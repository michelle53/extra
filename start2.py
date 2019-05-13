from TCP_Receiver import TCP_Receiver

from TCP_Sender import TCP_Sender
import random

from scapy.all import *

sport = random.randint(1024,65535)

# SYN
ip=IP(src='127.0.0.1',dst='127.0.0.1')
SYN=TCP(sport=80,dport=80,flags='S',seq=100)
SYNACK=sr1(ip/SYN)

print(SYNACK)
# SYN-ACK
my_ack = SYNACK.seq + 1
ACK=TCP(sport=80, dport=80, flags='A', seq=101 , ack=my_ack)
send(ip/ACK)

payload = "something"
TCP_PUSH = TCP(sport=80, dport=80, flags="PA", seq=102, ack=my_ack)
send(ip/TCP_PUSH/payload)
reply = sr2(ip/TCP_PUSH/payload, timeout=10)
