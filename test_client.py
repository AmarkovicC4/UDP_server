import socket 
import time

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 5005))
message1 = b"control4"
message2 = b"Hello C4 + SnapAV"
while True:
    client.sendto(message1, ('<broadcast>', 5005))
    client.sendto(message2, ('<broadcast>', 5005))
    print( message1 , message2 )
    time.sleep(1)

