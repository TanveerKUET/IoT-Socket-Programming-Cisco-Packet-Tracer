import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)  # Time from 0 to 10
ax.set_ylim(-10, 40)  # Temperature range

# Initialize empty data for plotting
time_data = []
temperature_data = []

# Create a line plot (initially empty)
line, = ax.plot([], [], lw=2)

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot
def update(frame):
    time_data.append(frame)
    # Simulate temperature data (you can replace this with real data)
    temperature = 20 + 5 * np.sin(0.5 * np.pi * frame)  # Example temperature function
    temperature_data.append(temperature)

    # Update the plot with the new data
    line.set_data(time_data, temperature_data)
    return line,

# Set up the animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 200),
                    init_func=init, blit=True)

plt.title('Dynamic Temperature vs Time')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.show()
