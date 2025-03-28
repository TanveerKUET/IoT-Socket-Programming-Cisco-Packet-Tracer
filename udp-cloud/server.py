import socket
HOST ='localhost'                                       # Server IP
PORT = 45000                                            # Server PORT
BUF_SIZE = 1024                                         # Buffer Size

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # initialize a socket object
s.bind((HOST,PORT))                                     # register port with OS
print("I am waiting for a client ...")

while True:                                             # wait for a connection
    data, addr = s.recvfrom(BUF_SIZE)                   # accept connection and retrieve conn object and address
    data = data.decode()                                # Process the received data
    print('I received '+ str(data)+ ' from ',addr)
    data=str(data).upper()                              # convert data to upper case
    s.sendto(data.encode(), addr)                       # send data back










