import socket
import random
import time 
import struct

SERVER = '192.168.1.200'
PORT = 6787
HEADER = 64
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)

PACKET_ID = 3

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
    
#acceleration = []
for value in random.sample(range(1,1000), 100):  
#    acceleration.append(values)
#    n = 3
#    for index in range(0,len(acceleration), n):
#        acceleration.append(acceleration[index:index+n])
    size = struct.calcsize(">Llf")
    data = struct.pack(">Llf",size,PACKET_ID,value)
    client.sendall(data)
    print(size, data.hex(' '), sep=", ")
    time.sleep(0.1)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST,PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))
