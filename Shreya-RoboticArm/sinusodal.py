import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Function to generate a sinusoidal wave
def generate_wave(x, frequency, amplitude):
    return amplitude * np.sin(2 * np.pi * frequency * x)

# Function to update the plot for each animation frame
def update(frame, line, x):
    line.set_ydata(generate_wave(x + frame / 10, frequency=1, amplitude=1))
    return line,

# Set up the figure and axis
fig, ax = plt.subplots()
x = np.linspace(0, 4 * np.pi, 1000)
line, = ax.plot(x, generate_wave(x, frequency=1, amplitude=1))

# Set axis limits
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-1.5, 1.5)

# Create the animation
ani = animation.FuncAnimation(fig, update, fargs=(line, x),
                              frames=200, interval=50, blit=True)

plt.title('Sinusoidal Wave Simulation')
plt.xlabel('X')
plt.ylabel('Amplitude')
plt.show()
