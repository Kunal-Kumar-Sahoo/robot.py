import matplotlib.pyplot as plt
import numpy as np

def draw_indian_flag(ax):
    # Draw the green rectangle (bottom)
    ax.add_patch(plt.Rectangle((0, 0), 3, 1, color='forestgreen'))

    # Draw the white rectangle (middle)
    ax.add_patch(plt.Rectangle((0, 1), 3, 1, color='white'))

    # Draw the saffron rectangle (top)
    ax.add_patch(plt.Rectangle((0, 2), 3, 1, color='#FF9933'))

    # Draw the navy blue Ashoka Chakra (circle in the middle)
    chakra = plt.Circle((1.5, 1.5), 0.15, color='navy', fill=False, linewidth=3)
    ax.add_patch(chakra)

    # Draw the 24 spokes of the Ashoka Chakra
    for i in range(24):
        angle = np.deg2rad(i * 15)
        x1, y1 = 1.5 + 0.15 * np.cos(angle), 1.5 + 0.15 * np.sin(angle)
        x2, y2 = 1.5 + 0.75 * np.cos(angle), 1.5 + 0.75 * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], color='navy', linewidth=3)

# Set up the figure and axis
fig, ax = plt.subplots()
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)

# Draw the Indian flag
draw_indian_flag(ax)

plt.axis('off')  # Turn off axis labels and ticks
plt.title('Indian Flag')
plt.show()
