import socket
import random
import time 
#import pickle

#(your_int_variabe).to_bytes(2, byteorder='big')

SERVER = '192.168.1.200'
PORT = 7779
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.sendall((100).to_bytes(4, byteorder='big'))
    string_to_bytes = (3).to_bytes(4, byteorder='big')
    client.send(string_to_bytes)
    client.sendall(message)
    #print(client.recv(2048).decode(FORMAT))
    
    
#acceleration = []
for values in random.sample(range(1,1000), 100):  
#    acceleration.append(values)
#    n = 3
#    for index in range(0,len(acceleration), n):
#        acceleration.append(acceleration[index:index+n])
    string_for_stream = str(values)
    send(string_for_stream)
    print(string_for_stream)
    time.sleep(0.1)

send(DISCONNECT_MESSAGE)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST,PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))
