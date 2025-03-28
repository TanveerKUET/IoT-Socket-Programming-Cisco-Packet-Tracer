import socket

def connect_to_server():
    server_ip = "127.0.0.1"  # Localhost (same machine)
    server_port = 12345  # Port number

    # Create a socket to connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Receive welcome message from the server
    welcome_message = client_socket.recv(1024)
    print(welcome_message.decode('utf-8'))

    while True:
        # Send a message to the server
        #message = input("You: ")
        #client_socket.send(message.encode('utf-8'))

        # Receive the response from the server (data from other client)
        response = client_socket.recv(1024)
        print("Other Client:", response.decode('utf-8'))

        # If the message is "exit", disconnect from the server
        #if message.lower() == "exit":
        #    break

    # Close the socket when done
    client_socket.close()

if __name__ == "__main__":
    connect_to_server()
