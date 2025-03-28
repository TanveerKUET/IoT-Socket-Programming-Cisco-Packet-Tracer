import socket
import threading

# Global list to store connected clients
clients = []

# Function to handle communication with clients
def client_thread(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")

    # Send a welcome message to the client
    client_socket.send(b"Hello, you are connected to the server!\n")

    # Add the client to the list of connected clients
    clients.append(client_socket)

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            print(data)
            # If client sends no data (client disconnected), break the loop
            if not data:
                break

            # Broadcast the received data to all other clients (except the sender)
            forward_data_to_other_clients(data, client_socket)
            print("forwarding to client 2: "+str(data))
    except Exception as e:
        print(f"Error with client {client_address}: {e}")

    finally:
        # Remove client from the list when done
        clients.remove(client_socket)
        client_socket.close()
        print(f"Connection with {client_address} closed.")

# Function to forward data to all other connected clients
def forward_data_to_other_clients(data, sender_socket):
    for client_socket in clients:
        if client_socket != sender_socket:  # Don't send the data back to the sender
            try:
                client_socket.send(data)  # Send the data to the other client
            except Exception as e:
                print(f"Error sending data to a client: {e}")

def start_server():
    # Server setup
    server_ip = "127.0.0.1"  # Localhost IP
    server_port = 12345  # Port number

    # Create the socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(2)  # Listen for up to 2 clients
    print(f"Server is listening on {server_ip}:{server_port}...")

    # Accept connections from clients in a loop
    while len(clients) < 2:  # Only accept 2 clients
        client_socket, client_address = server_socket.accept()
        # Create a new thread to handle each client
        thread = threading.Thread(target=client_thread, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
