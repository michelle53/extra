from TCP_Receiver import TCP_Receiver
from TCP_Sender import TCP_Sender

snd = TCP_Sender()
rc = TCP_Receiver()

rc.start()

snd.start(snd,"127.0.0.1")


