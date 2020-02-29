import pygame, glob, os, re
from bin.lib.Level import Level, Tile
from bin.config.levelCFG import LEVEL_DIR
class Levelmanager:
    Levels = [Level] 
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

    
    
    def load_levels(self, dir = LEVEL_DIR):
        lvlPaths = os.listdir(LEVEL_DIR) #to be tested
        #lvlFilePaths = glob.glob(LEVEL_DIR + '[0-9][0-9][0-9]') #deprectated, too complicated, /wo need
        #lvlFilePaths.sort()
        for singleLvlPath in lvlPaths:  #jeden Ordner in lvl/ einbeziehen
            LvlFilePaths = glob.blod(os.path.join(singleLvlPath, '') + '*.lvl')
            for singleLvlFilePath in LvlFilePaths:  #wenn in einem Ordner mehrere .lvl Dateien existieren, dann lade diese als individuelle Lvl
                newLevel = Level()
                newLevel.parseFile(singleLvlFilePath)


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