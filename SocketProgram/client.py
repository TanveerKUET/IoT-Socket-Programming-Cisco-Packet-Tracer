import socket
HOST ='localhost'                                       # Server IP
PORT = 45000                                            # Server PORT
BUF_SIZE = 1024                                         # Buffer Size
message = "Hi COE 550!"

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)    # initialize a socket object
s.connect((HOST,PORT))                                  # connect to server

s.sendall(message.encode())                             # send message

data = s.recv(BUF_SIZE).decode()                        # wait to receive a message
print('received: '+ str(data))

s.close()                                               # close connection
print("Bye")
