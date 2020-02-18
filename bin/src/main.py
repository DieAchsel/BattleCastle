import os

import pygame

# Constanses
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750



# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background
background = pygame.image.load(os.path.join('../img/bg/02', '02Full.png'))

# Caption and Icon
pygame.display.set_caption("Battle Castle")
icon = pygame.image.load(os.path.join('../img/icon', 'castle.png'))
pygame.display.set_icon(icon)

#GameLoop
running = True
while running:

    # Set Bacjground
    screen.blit(background, (0, 0))

    # Handle Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False



    # update Screen
    pygame.display.update()