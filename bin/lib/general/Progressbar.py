#Hier entsteht ein Progressbar objekt, welches von surface erbt und mit setProgress(int = [0-100]) angesprochen werden
#Der Progressbar besteht aus einem Surface-Objekt, welches den eigentlichen Progressbar maskiert. 
#Der eigentliche Progressbar besteht aus 2 surfaces dem loaded- und unloaded-Teil. in der Summe haben diese beiden Balken immer die selbe Breite. 
#Es werden wenn möglich vorhandene TIle-Texturen zur gestaltung verwendet und je nach level gewechselt
import pygame

class Progressbar(pygame.sprite.Sprite):
    progress = 0
    loadedTexture = pygame.image
    unloadedTexture = pygame.image
    innerBorderTexture = pygame.image
    innerCornerTexture = pygame.image

    def __init__(self, newRect = DEFAULT_SIZE, newProgress = DEFAULT_PROGRESS):
        self.image = pygame.surface()
        super().__init__()
        self.rect = newRect
