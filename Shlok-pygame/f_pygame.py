from sys import exit 
import pygame

pygame.init() #start and initialize pygame 

#Display surface: we need a game window on which we will be displaying the elements of game 

screen = pygame.display.set_mode((800,400))

pygame.display.set_caption('non')

clock = pygame.time.Clock()



while True: 
    #draw our elements 
    #update everything

    pygame.display.update() 


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(60)


