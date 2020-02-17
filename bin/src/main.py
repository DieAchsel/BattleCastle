import pygame, os

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Battle Castle")

icon = pygame.image.load(os.path.join('../img/icon', 'castle.png'))

pygame.display.set_icon(icon)

#GameLoop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False