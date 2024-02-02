import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Function to update the snowfall animation
def update(frameNum, points, N, snowfall):
    # Update the position of each snowflake
    snowfall[:, 1] -= 0.1  # Move the snowflakes downward
    snowfall[snowfall[:, 1] < 0, 1] = N  # Respawn snowflakes at the top when they go below the screen
    points.set_offsets(snowfall)

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Generate initial positions for the snowflakes
N = 100
snowfall = 10 * np.random.rand(N, 2)
snowfall[:, 0] = np.random.rand(N) * 10

# Create scatter plot for snowflakes
points = ax.scatter(snowfall[:, 0], snowfall[:, 1], marker='*', color='white', s=50)

# Create the animation
ani = animation.FuncAnimation(fig, update, fargs=(points, 10, snowfall), frames=100, interval=100, blit=False)

# Set the background color to represent the night sky
fig.patch.set_facecolor('blue')
ax.set_facecolor('blue')

plt.title('Christmas Snowfall Simulation')
plt.show()
