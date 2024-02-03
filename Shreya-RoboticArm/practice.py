import pygame 
import math
import numpy as np

#define variables
screen_width=600
screen_height=600
ball_radius=20
paddle_width=100
paddle_height=20

#initiaalise pygame
pygame.init()
screen=pygame.display.set_mode((screen_height,screen_width))
pygame.display.set_caption("Shreyaa Screen")
clock=pygame.time.Clock()


pygame.display.flip()
clock.tick(60)
