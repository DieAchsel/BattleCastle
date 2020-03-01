import pygame, glob, os, re
from bin.lib.Level import Level, Tile
from bin.config.levelCFG import LEVEL_DIR, DEFAULT_LOADING_SPINNER_PATH
#Der LevelManager kann eigenlich in die Klasse BattleCastle umgewandelt werden, es müssen nurnoch die player Objekte von Alex eingebunden werden
class BattleCastle:
    Levels = [Level] 
    activeLevel = 0 #aktuelle Position in der levelListe
    loadedTiles = [Tile]#DEPRECATED #Liste aller geladenen TileObjekte (eigentlich unnötig da genau das die spritegroups machen)
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
    #hier wird ein neues LevelObjekt erwartet
    def add(self, newLevel):
        pass
    #hier wird eine Liste aus levelObjekten erwartet
    def add(self, newLevels = []):
        pass
    #hier wird ein directory mit .lvl Datei erwartet
    def add(self, dir):
        pass
    #hier wird ein directory mit directories erwartet.
    def add(self, dir):
        pass
    
    def get_loading_spinner(self):
        if(os.path.isfile(DEFAULT_LOADING_SPINNER_PATH)):
            spinner = pygame.image.load(DEFAULT_LOADING_SPINNER_PATH)
            return spinner
    
    def load_levels(self, dir = LEVEL_DIR):
        lvlPaths = os.listdir(LEVEL_DIR) #to be tested
        #lvlFilePaths = glob.glob(LEVEL_DIR + '[0-9][0-9][0-9]') #deprectated, too complicated, /wo need
        #lvlFilePaths.sort()
        for singleLvlPath in lvlPaths:  #jeden Ordner in lvl/ einbeziehen
            LvlFilePaths = glob.blod(os.path.join(singleLvlPath, '') + '*.lvl')
            for singleLvlFilePath in LvlFilePaths:  #wenn in einem Ordner mehrere .lvl Dateien existieren, dann lade diese als individuelle Lvl
                newLevel = Level()
                newLevel.parseFile(singleLvlFilePath)

    def set_loading_screen(self, FilePath = DEFAULT_LOADING_SCREEN_PATH):
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