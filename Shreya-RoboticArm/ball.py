import pygame
import math
import numpy as np

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

clock = pygame.time.Clock()  # control frame rate

# Ball properties
ball_x = SCREEN_WIDTH //2
ball_y = SCREEN_HEIGHT //2
ball_speed_x = 5
ball_speed_y = 5

# Paddle properties
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle with the mouse
    paddle_x, _ = pygame.mouse.get_pos()
    paddle_x -= PADDLE_WIDTH // 2
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x > SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce off the walls
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Bounce off the paddle
    if (
        paddle_x < ball_x < paddle_x + PADDLE_WIDTH
        and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT
    ):
        ball_speed_y = -ball_speed_y

    # Check for game over (ball went below the paddle)
    if ball_y > SCREEN_HEIGHT:
        ball_x = SCREEN_WIDTH // 2
        ball_y = SCREEN_HEIGHT // 2
        ball_speed_x = 5
        ball_speed_y = 5

    screen.fill((135, 206, 250))  # Set sky blue background

    # Draw the paddle
    pygame.draw.rect(screen, (0, 0, 0), (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw the ball
    pygame.draw.circle(screen, (255, 0, 0), (int(ball_x), int(ball_y)), BALL_RADIUS)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
