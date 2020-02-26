import pygame
from bin.lib.Level import Level
from bin.lib.Level import Tile
class Levelmanager:
    Levels = {Level} 
    activeLevel = Level
    loadedTilesY = [Tile]
    loadedLevel = pygame.sprite.sprite.pygame.sprite.Group
    harmfulTiles = pygame.sprite.sprite.pygame.sprite.Group
    collidableTiles = pygame.sprite.sprite.pygame.sprite.Group
    animatedTiles = pygame.sprite.sprite.pygame.sprite.Group


    def __init__(self):
        super().__init__()

    def calcTileSize(self, PlayArea = {"X": DEFAULT_PLAYAREA_X, "Y": DEFAULT_PLAYAREA_Y}):
        pass

    def build(self):
        pass

    def add(self, newLevel):
        pass

    def add(self, newLevels = []):
        pass

    def add(self, newFile):
        pass

    def add(self, newFiles):
        pass

    def load(self, levelID = activeLevel.getID() + 1):
        pass

    def save(self):
        #In Zukunft sollen hier selbst erstellte Level gespeichert werden können
        pass

    def create(self):
        #In Zukunft soll der Nutzer eigene Level erstellen können.
        #Da dies ein "NiceToHave"-Feature ist wird dies zunächst nicht implementiert
        pass

    def getLoadedSprites(self):
        return loadedLevel

    def isColliding(self, object = pygame.sprite.sprite):
        return pygame.sprite.spritecollide(object, loadedLevel).len > 0