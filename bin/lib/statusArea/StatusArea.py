#
import pygame
from bin.lib.Level import Tile
from bin.config.generalCFG import SCREEN_SIZE, COLORKEY
from bin.config.statusAreaCFG import STATUS_AREA, DEFAULT_LAYER

class StatusArea(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([STATUS_AREA.w, STATUS_AREA.h], depth = 24)
        self.rect = STATUS_AREA
        self.layer = DEFAULT_LAYER
        self.Objects = pygame.sprite.Group()
    
    def add(self, newObj = pygame.sprite.Sprite):
        self.Objects.add(newObj)


#ToDo: StatusArea benötigt noch eine Funktion zum angleichen der Rastergröße des Hintergrundes an die tilegröße
    def set_texture(self, newTexture = tile):
        pass