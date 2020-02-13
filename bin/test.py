import pygame
from pygame.locals import *
#Initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Battle Castle")

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    



# Icon by Smashicons <- Info für die Doku | Bereich source