import pygame, glob, os, re
from bin.lib.Level import Level, Tile
from bin.lib.Player import Player
from bin.config.levelCFG import LEVEL_DIR, DEFAULT_LOADING_SPINNER_PATH
from bin.config.generalCFG import *
#Das gesamte BattleCastle Game kann rheintheoretisch ein sprite sein, wodurch dem pygameDisplay nurnoch ein Objekt vom Typ BattleCastle übergeben wird und alles durch dessen updateMethode abläuft
class BattleCastle(pygame.sprite.Sprite):
    Levels = [Level] 
    activeLevel = 0 #aktuelle Position in der levelListe
    loadedTiles = [Tile]#DEPRECATED #Liste aller geladenen TileObjekte (eigentlich unnötig da genau das die spritegroups machen)
    loadedLevel = pygame.sprite.Group
    harmfulTiles = pygame.sprite.Group #ggfs falsch geschrieben
    collidableTiles = pygame.sprite.Group
    animatedTiles = pygame.sprite.Group
    players = pygame.sprite.Group
    players = []
    isLoading = False
    def __init__(self, screen = pygame.surface([SCREEN_SIZE["X"], SCREEN_SIZE["Y"]], depth = 24)):
        super().__init__()
        DEBUG("********************Debugging Aktiv********************\nSpiel-Version = " + str(VERSION) + "\nSpielverzeichnis = " + GAME_DIR + "\nDebug-Level = " + str(DEBUG_LEVEL) + "\n\n\n")

        
    
    #Zeichne Alle spritegruppen mit group..draw auf die battleCastle Surface
    def draw(self, screen):
        pass

    def update(self):
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
        pass
    pygame.quit()

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

    #durchsucht das Level-Verzeichnis und erstellt für jeden gefundenen Ordner ein Level
    def load_levels(self):
        set_loading_screen()    #Das Laden der Level könnte dauern
        lvlPaths = os.listdir(LEVEL_DIR)
        for singlePath in lvlPaths:
            #Wenn der betrachtete Ordner eine .lvl Datei enthält, dann erstelle ein neues Level
            if(len(glob.blod(os.path.join(singlePath, '') + '*.lvl')) > 0): 
                level = Level(singlePath)

    #erstellt einen Ladebildschirm und fügt in Mittig auf der PlayArea ein
    def set_loading_screen(self, FilePath = DEFAULT_LOADING_SCREEN_PATH):
        self.isLoading = True
        pass
    #entfernt den LadeBildschirm, sofern aktiv
    def unset_loading_screen(self):
        self.isLoading = False
        pass
    def save(self):
        #In Zukunft sollen hier selbst erstellte Level gespeichert werden können
        pass

    def create(self):
        #In Zukunft soll der Nutzer eigene Level erstellen können.
        #Da dies ein "NiceToHave"-Feature ist wird dies zunächst nicht implementiert
        pass
    #gibt eine spriteGroup mit dem gesamten geladenen Level zurück
    def getLoadedSprites(self):
        return loadedLevel

    def isColliding(self, object = pygame.sprite.sprite):
        return pygame.sprite.spritecollide(object, loadedLevel).len > 0