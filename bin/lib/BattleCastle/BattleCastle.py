import pygame, glob, os, re
from bin.lib.Level import Level, Tile
from bin.lib.Player import Player
from bin.config.levelCFG import LEVEL_DIR, DEFAULT_LOADING_SPINNER_PATH
from bin.config.generalCFG import *
#Das gesamte BattleCastle Game kann rheintheoretisch ein sprite sein, wodurch dem pygameDisplay nurnoch ein Objekt vom Typ BattleCastle übergeben wird und alles durch dessen updateMethode abläuft
class BattleCastle(pygame.sprite.Sprite):
    Levels = [Level] 
    activeLevel = 0 #aktuelle Position in der levelListe
    #loadedTiles = [Tile]#DEPRECATED #Liste aller geladenen TileObjekte (eigentlich unnötig da genau das die spritegroups machen)
    loadedLevel = pygame.sprite.Group
    allSprites = pygame.sprite.Group
    harmfulTiles = pygame.sprite.Group
    collidableTiles = pygame.sprite.Group
    animatedTiles = pygame.sprite.Group
    players = pygame.sprite.Group
    players = []
    isLoading = False
    def __init__(self, screen = pygame.surface([SCREEN_SIZE["X"], SCREEN_SIZE["Y"]], depth = 24)):
        super().__init__()
        DEBUG("********************Debugging Aktiv********************\nSpiel-Version = " + str(VERSION) + "\nSpielverzeichnis = " + GAME_DIR + "\nDebug-Level = " + str(DEBUG_LEVEL) + "\n\n\n")

    def update(self):
        #animatedTiles gruppe updaten

        #Playergruppe updaten
        pass

    def calcTileSize(self, PlayArea = {"X": DEFAULT_PLAYAREA_X, "Y": DEFAULT_PLAYAREA_Y}):
        pass
    
    def draw(self, surface):
        self.allSprites.draw(surface)
        return surface

    def draw(self):
        self.allSprites.draw(self.image)
        self.rect = self.image.get_rect()  

    #Zurückgestellt-----
        #hier wird ein neues LevelObjekt erwartet
        #def add(self, newLevel):
        #    pass
        #hier wird eine Liste aus levelObjekten erwartet
        #def add(self, newLevels = []):
        #    pass
        #hier wird ein directory mit .lvl Datei erwartet
        #def add(self, dir):
        #    pass
        #hier wird ein directory mit directories erwartet.
        #def add(self, dir):
        #    pass
    #-----Zurückgestellt
    

    #durchsucht das Level-Verzeichnis und erstellt für jeden gefundenen Ordner ein Level
    def load_levels(self):
        self.load_loading_spinner()    #Das Laden der Level könnte dauern
        lvlPaths = os.listdir(LEVEL_DIR)
        for singlePath in lvlPaths:
            #Wenn der betrachtete Ordner eine .lvl Datei enthält, dann erstelle ein neues Level
            #ist das so richtig mit path..join??
            if(len(glob.glod(os.path.join(singlePath, '') + '*.lvl')) > 0):
                level = Level(singlePath)

    #erstellt einen Ladebildschirm und fügt in Mittig auf der PlayArea ein
    def set_loading_spinner(self, FilePath = DEFAULT_LOADING_SCREEN_PATH):
        self.isLoading = True
        pass
    #entfernt den LadeBildschirm, sofern aktiv
    #UNFERTIG
    def unset_loading_spinner(self):
        self.isLoading = False
        pass

    def load_loading_spinner(self, FilePath = ""):
        if(os.path.exists(FilePath)):
            #UNFERTIG
            pass
        else:
            if(os.path.isfile(DEFAULT_LOADING_SPINNER_PATH)):
                spinner = pygame.image.load(DEFAULT_LOADING_SPINNER_PATH)
                return spinner
    #Zurückgestellt-----
        #def save(self):
        #    #In Zukunft sollen hier selbst erstellte Level gespeichert werden können
        #    pass

        #def create(self):
        #    #In Zukunft soll der Nutzer eigene Level erstellen können.
        #    #Da dies ein "NiceToHave"-Feature ist wird dies zunächst nicht implementiert
        #    pass
    #-----Zurückgestellt

    #WIRKLICH BENÖTIGT?:
    #gibt eine spriteGroup mit dem gesamten geladenen Level zurück
    def get_loaded_level(self):
        return self.loadedLevel

    def get_loaded_sprites(self):
        return self.allSprites

    def isColliding(self, object = pygame.sprite.sprite):
        return pygame.sprite.spritecollide(object, self.loadedLevel)
    def isColliding(self, object = pygame.sprite.group):
        return pygame.sprite.groupcollide (object, self.loadedLevel)