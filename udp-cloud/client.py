import socket
HOST ='localhost'                                           # Server IP
PORT = 45000                                                # Server PORT
BUF_SIZE = 1024                                             # Buffer Size
message = "Hi there!"

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)        # initialize a socket object
s.sendto(message.encode(), (HOST,PORT))                     # send message

data = s.recv(BUF_SIZE)                                     # wait to receive a message
print('received '+ str(data.decode()))
print("Bye")
