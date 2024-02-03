from sys import exit 
import pygame

pygame.init() #start and initialize pygame 

#Display surface: we need a game window on which we will be displaying the elements of game 

screen = pygame.display.set_mode((800,400))
#paddle_surface = pygame.Surface((60,10))
#paddle_surface.fill('red')
pygame.display.set_caption('non')

clock = pygame.time.Clock()



while True: 
    #draw our elements 
    #update everything

    pygame.display.update() # updates everything while going through the for loop everytime 

    # at this point if we run code we wouldn't be able to close our code, infinte hang state mai chaa jayega 
    # thus we need a closing feature 
    # we use exit() from sys library to close all kinds of code
    # but first we need to get any type of input user is entering and interpret it 
    # here comes the EVENT LOOP

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #pygame.draw.circle(screen,'red',(40,40),10)
    #pygame.draw.rect(screen,'blue',(50,50,100,300))
    #pygame.draw.line(screen, 'white',(200,200), (300,300), 5)

    #screen.blit(paddle_surface,(350,380))
    clock.tick(60)


