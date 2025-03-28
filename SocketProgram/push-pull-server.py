import socket
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Server settings
HOST = '127.0.0.1'  # Localhost for testing
PORT_CLIENT_1 = 44444    # MCU 1 will connect to this port
PORT_CLIENT_2 = 55555    # MCU 2 will connect to this port
BUFFER_SIZE = 1024  # Adjust based on expected data size

# Create the server socket for client 1
server_socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_1.bind((HOST, PORT_CLIENT_1))  # Bind to a specific port for the server
server_socket_1.listen(2)
print(f"Server listening on {HOST}:{server_socket_1.getsockname()[1]}")

# Create the server socket for client 2
server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_2.bind((HOST, PORT_CLIENT_2))  # Bind to a specific port for the server
server_socket_2.listen(2)
print(f"Server listening on {HOST}:{server_socket_2.getsockname()[1]}")


# Accept two client connections
def start_server():
    client_1_socket, addr_1 = server_socket_1.accept()
    print(f"Client 1 connected from {addr_1}")
    client_2_socket, addr_2 = server_socket_2.accept()
    print(f"Client 2 connected from {addr_2}")

    i = 1
    while True:
        # Send request to client 1 every 100ms
        client_1_socket.sendall(b"PULL")
        print(f"PULL request: {i}")

        # Receive temperature and CO level data from Client 1
        data = client_1_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"Received from Client 1: {data.decode()}\n")

        # Send the received data back to Client 2
        #client_2_socket.sendall(f"{data.decode()}".encode())
        if(i%2==0):
            CMD = "FS:WC"
        if(i%2 !=0):
            CMD = "FF:WO"
        client_2_socket.sendall(CMD.encode())
        # Receive acknowledgment from Client 2
        data = client_2_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"ACK from Client 2: {data.decode()}")

        # Increment iteration count
        i += 1
        time.sleep(1)  # Sleep for 100ms

if __name__ == "__main__":
    start_server()