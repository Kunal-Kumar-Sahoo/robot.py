import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame Simulation")

# Set up the square
square_size = 50
square_color = (0, 0, 255)
square_position = [width // 2, height // 2]

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update square position
    square_position[0] += 5  # Move the square 5 pixels to the right

    # Reset square position when it goes beyond the right edge
    if square_position[0] > width:
        square_position[0] = -square_size

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the square
    pygame.draw.rect(screen, square_color, (square_position[0], square_position[1], square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)
