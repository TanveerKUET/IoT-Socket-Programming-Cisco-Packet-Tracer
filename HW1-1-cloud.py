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

# Threshold values
TEMP_THRESHOLD = 50  # Temperature in °C
CO_THRESHOLD = 5  # CO Level

# Sensor Data Storage
sensor_data = {"temperature": [], "co": []}
control_data = {"fan": [], "window": []}
# Create a figure for live plotting
fig, ax = plt.subplots()

def update_graph(i):
    ax.clear()  # Clear the previous plot
    ax.plot(sensor_data["temperature"], label="Temperature (°C)")
    ax.plot(sensor_data["co"], label="CO Level")
    ax.plot(control_data["fan"], label="FAN: LOW/HIGH")
    ax.plot(control_data["window"], label="WINDOW: OPEN/CLOSE")
    ax.legend()
    ax.set_title("Sensor Readings and actuators outcomes")
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")

# Live Plotting Animation
ani = FuncAnimation(fig, update_graph, interval=1000, cache_frame_data=False)

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
        Temp, CO = data.decode().split(';')
        Temperature, tempvalue = Temp.split(':')
        CarbonMonoxide, covalue = CO.split(':')

        # Store data for visualization
        sensor_data["temperature"].append(float(tempvalue))
        sensor_data["co"].append(float(covalue))

        ########Send controlling commands to MCU 2 here##########
        print("Temp: " + str(tempvalue))
        print("CO: " + str(covalue))
        tempvalue = float(tempvalue)
        covalue = float(covalue)

        FanStatus = ""
        WindowStatus = ""
        if (tempvalue < 50):
            print("FAN RUNNING LOW")
            FanStatus = "FL"
            control_data["fan"].append(5)
        if (tempvalue > 50):
            print("FAN RUNNING FAST")
            FanStatus = "FF"
            control_data["fan"].append(20)
        if (covalue > 20):
            print("WINDOW OPEN")
            WindowStatus = "WO"
            control_data["window"].append(30)
        if (covalue < 20):
            print("WINDOW CLOSED")
            WindowStatus = "WC"
            control_data["window"].append(10)

        MSG = FanStatus + ";" + WindowStatus
        print("SENT COMMANDS TO MCU 2: "+MSG)
        ################
        # Send the received data back to Client 2
        #client_2_socket.sendall(f"{data.decode()}".encode())

        client_2_socket.sendall(MSG.encode())
        # Receive acknowledgment from Client 2
        data = client_2_socket.recv(BUFFER_SIZE)
        if not data:
            break
        print(f"ACK from Client 2: {data.decode()}")

        # Increment iteration count
        i += 1
        time.sleep(0.1)  # Sleep for 100ms

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True  # Allow program to exit even if the server is running
server_thread.start()

# Show the plot window
plt.show()
