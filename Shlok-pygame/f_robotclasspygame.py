import pygame
from sys import exit

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

pygame.init()

# Setting up the display window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pygame Simulation with Classes")

pygame.time.Clock()

# Create a robot instance (from Robot class created earlier)
my_robot = Robot(100, 100)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

    # moving the robot
    my_robot.move(0, 0)

    # drawing the robot on screen
    screen.fill((255, 255, 255)) 
    pygame.draw.rect(screen, (0, 0, 0), (my_robot.x, my_robot.y, 50, 50))

    pygame.time.Clock().tick(69)
    # Update the display
    pygame.display.flip()

