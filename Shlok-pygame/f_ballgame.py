import pygame
import sys

# Initializing Pygame library
pygame.init()

# Setting up the display screen on which our simulation will be dispayed (Canvas)
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball Bouncing Game")

# Colors to be used in game (R,G,B)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Class creation for Balls
class Ball:
    def __init__(self, x, y, radius, speed, dir_x, dir_y, color): #initialzation funciton for every ball that we define (instance)
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color

    def move(self):
        self.x += self.speed * self.dir_x
        self.y += self.speed * self.dir_y
        # The parameters above get updated in every loop forming a kind of animation 
        
        # Bounce off side and top walls (screen bounds)
        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.dir_x *= -1
        if self.y - self.radius <= 0:
            self.dir_y *= -1
        elif self.y + self.radius >= height:
            # Reset the ball to its initial position if it goes below the paddle
            self.x = 300
            self.y = self.radius

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # draws a circle (game ball) with given values and position

# Paddle details
paddle_width = 100
paddle_height = 10

# Initial paddle positions
paddle_x = (width - paddle_width) // 2
paddle_y = height - 20

# Create instances of the Ball class
ball1 = Ball(300, 200, 10, 5, 1, 1, 'red')
ball2 = Ball(100, 100, 10, 3, -1, -1,'yellow')

# score counter
score = 0

# Font for displaying score
font = pygame.font.Font(None, 36)

# Main game loop
while True:
    # exit condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # why? if we already used pygame.quit()

    # Moving the paddle based on mouse movement - update x coordinate of the paddle
    paddle_x = pygame.mouse.get_pos()[0] - paddle_width // 2

    # Keeping the paddle within the screen boundaries
    if paddle_x < 0:
        paddle_x = 0
    elif paddle_x + paddle_width > width:
        paddle_x = width - paddle_width

    # Moving and bouncing the balls by calling the sel.move method from the class ball
    ball1.move()
    ball2.move()

    # Checking condition for collisions with the paddle for both balls
    if (
        paddle_x < ball1.x < paddle_x + paddle_width
        and paddle_y - ball1.radius < ball1.y < paddle_y
    ):
        ball1.dir_y *= -1
        score +=1

    if (
        paddle_x < ball2.x < paddle_x + paddle_width
        and paddle_y - ball2.radius < ball2.y < paddle_y  
    ):
        ball2.dir_y *= -1
        score +=1        

    # Clear the screen .. maybe?
    screen.fill((0, 0, 0))

    # Drawing the paddle and balls
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    ball1.draw()
    ball2.draw()
    #pygame.draw.line(screen, WHITE,(0,paddle_y - ball1.radius),(width,paddle_y - ball1.radius))

    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate..importance?
    pygame.time.Clock().tick(60)
