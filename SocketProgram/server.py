import socket
HOST ='localhost'   # Server IP
PORT = 45000        # Server PORT
BUF_SIZE = 1024     # Buffer Size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # initialize a socket object
s.bind((HOST,PORT))                                         # register port with OS
print("I am waiting for a client ...")
s.listen(2)                                     # wait for a connection (maximum of 1 connection)

conn, add = s.accept()                          # accept connection and retrieve conn object and address
print("I got a connection form ",add)

while True:
    data = conn.recv(BUF_SIZE).decode()         # check if data accepted
    if not data:                                # no data, pass
        break
    print('I received '+ str(data))             # received data
    data=str(data).upper()                      # convert data to upper case
    conn.sendall(data.encode())
conn.close()










# send data back
# close connection
