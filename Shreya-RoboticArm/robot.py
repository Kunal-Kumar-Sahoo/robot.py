
import pygame
import math
import numpy as np

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BASE_SIZE = 50
JOINT_RADIUS = 10
LINK_LENGTH_1 = 100
LINK_LENGTH_2 = 100
ACTUATOR_WIDTH = 8
END_EFFECTOR_SIZE = 20
TABLE_WIDTH = 200
TABLE_HEIGHT = 20

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robotic Arm Simulation")

font = pygame.font.Font(None, 24)

clock = pygame.time.Clock()

# Function to calculate inverse kinematics with constraints
 #..........
   # ....
   # ....
   # ....

    # Check if the target is within the reachable workspace
    #.....
    #......

    #.......
    #......
    #.....
    
    # Calculate theta1 without constraints
    #.......

    # Apply constraints to theta1
    #........

    # Calculate the end effector position
    #......
    #.....

    # Check if the end effector is below the table
    #.......
    #.....
    #......

# Function to draw the robotic arm
def draw_arm(base_x, base_y, theta1, theta2):
    joint1_x = base_x + LINK_LENGTH_1 * np.cos(theta1)
    joint1_y = base_y + LINK_LENGTH_1 * np.sin(theta1)

    end_x = joint1_x + LINK_LENGTH_2 * np.cos(theta1 + theta2)
    end_y = joint1_y + LINK_LENGTH_2 * np.sin(theta1 + theta2)

    pygame.draw.rect(screen, (0, 0, 0), (base_x - BASE_SIZE // 2, base_y - BASE_SIZE // 2, BASE_SIZE, BASE_SIZE))
    pygame.draw.circle(screen, (0, 0, 0), (base_x, base_y), JOINT_RADIUS)
    pygame.draw.line(screen, (0, 255, 0), (base_x, base_y), (joint1_x, joint1_y), ACTUATOR_WIDTH)
    pygame.draw.circle(screen, (0, 0, 0), (joint1_x, joint1_y), JOINT_RADIUS)
    pygame.draw.line(screen, (0, 255, 0), (joint1_x, joint1_y), (end_x, end_y), ACTUATOR_WIDTH)
    pygame.draw.rect(screen, (0, 0, 0), (end_x - END_EFFECTOR_SIZE // 2, end_y - END_EFFECTOR_SIZE // 2, END_EFFECTOR_SIZE, END_EFFECTOR_SIZE))

    # Display end effector coordinates and arm lengths in the right upper corner
    text = font.render(f"End Effector: ({end_x:.2f}, {end_y:.2f})", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (SCREEN_WIDTH - text_rect.width - 10, 10)
    screen.blit(text, text_rect)

    text = font.render(f"Arm Lengths: L1={LINK_LENGTH_1}, L2={LINK_LENGTH_2}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = (SCREEN_WIDTH - text_rect.width - 10, 40)
    screen.blit(text, text_rect)

# Function to draw the table
def draw_table(base_x, base_y):
    table_top_y = base_y + BASE_SIZE // 2
    pygame.draw.rect(screen, (139, 69, 19), (base_x - TABLE_WIDTH // 2, table_top_y, TABLE_WIDTH, TABLE_HEIGHT))

# Function to draw the grass
def draw_grass():
    pygame.draw.rect(screen, (0, 128, 0), (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2))

# Fixed initial angle for the first joint (upward 45 degrees)
theta1 = math.radians(-45)
# Initial angle for the second joint (set to 0 degrees initially)
theta2 = 0.0

# Capture mouse click coordinates
mouse_click_coordinates = None
# Counter for the number of clicks
click_counter = 0
# Maximum allowed clicks
max_clicks = 100
# Initialize joint_angles outside the loop
joint_angles = None

# Main simulation loop
running = True
out_of_reach_timer = 0  # Timer to control the display duration
out_of_reach_duration =0.5  # Duration to display "Out of Reach" in seconds

#whilee running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and click_counter < max_clicks:
            if event.button == 1:
                mouse_click_coordinates = event.pos
                click_counter += 1
# mouse click coordinates
    #......
     #......
      #......
       #.......

        if joint_angles is not None:
            theta1, theta2 = joint_angles
        else:
            # Set the timer to display "Out of Reach" in the middle for 2 seconds
            out_of_reach_timer = pygame.time.get_ticks()

    screen.fill((135, 206, 250))

    draw_grass()
    draw_table(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_arm(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, theta1, theta2)

    # Display "Out of Reach" under the brown table if joint_angles is None (out of reach)
    if joint_angles is None:
        current_time = pygame.time.get_ticks()
        if current_time - out_of_reach_timer < out_of_reach_duration * 1000:
            out_of_reach_text = pygame.font.Font(None, 36).render("Out of Reach", True, (255, 255, 255))  # White color
            out_of_reach_rect = out_of_reach_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + TABLE_HEIGHT + 50))
            screen.blit(out_of_reach_text, out_of_reach_rect)

    pygame.display.flip()
    clock.tick(60)

click_counter = 0

pygame.quit()
