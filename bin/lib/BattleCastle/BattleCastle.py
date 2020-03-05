import pygame, glob, os, re
from bin.lib.Level import Level
from bin.lib.Tile import Tile
from bin.lib.Player import Player
from bin.config.levelCFG import LEVEL_DIR, DEFAULT_LOADING_SPINNER_PATH
from bin.config.generalCFG import *


# Das gesamte BattleCastle Game kann rheintheoretisch ein sprite sein, wodurch dem pygameDisplay nurnoch ein Objekt vom Typ BattleCastle übergeben wird und alles durch dessen updateMethode abläuft
class BattleCastle(pygame.sprite.Sprite):
    def __init__(self, screen=pygame.surface([SCREEN_SIZE["X"], SCREEN_SIZE["Y"]], depth=24)):
        super().__init__()
        DEBUG("********************Debugging Aktiv********************\nSpiel-Version = " + str(
            VERSION) + "\nSpielverzeichnis = " + GAME_DIR + "\nDebug-Level = " + str(DEBUG_LEVEL) + "\n\n\n")
        self.levels = []
        self.error = False
        self.activeLevel = 0  # aktuelle Position in der levelListe
        self.loadedLevel = pygame.sprite.Group()
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.harmfulTiles = pygame.sprite.Group()
        self.collidableTiles = pygame.sprite.Group()
        self.animatedTiles = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.player1 = Player.Player(1, True)
        self.player2 = Player.Player(3, False)
        self.players.add(self.player1, self.player2)
        self.allSprites.add(players)
        self.isLoading = False
        self.load_levels()
        self.loadedLevel.add(self.levels[self.activeLevel].build())
        self.allSprites.add(self.loadedLevel)
    # durchsucht das Level-Verzeichnis und erstellt für jeden gefundenen Ordner ein Level
    def load_levels(self):
        self.load_loading_spinner()  # Das Laden der Level könnte dauern
        lvlPaths = os.listdir(LEVEL_DIR)
        if(len(lvlPaths) == 0):
            for singlePath in lvlPaths:
                #Wenn der betrachtete Ordner eine .lvl Datei enthält, dann erstelle ein neues Level
                #ist das so richtig mit path..join??
                foundLvlFiles = glob.glod(os.path.join(singlePath, '') + '*.lvl')
                if(len(foundLvlFiles > 0)):
                    for lvlFile in foundLvlFiles:
                        self.levels.append(Level(lvlFile))
                    self.activeLevel = 0
                else:
                    DEBUG("ES wurden keine LvlFiles gefunden", 2)
        else:
            DEBUG("ES wurden keine LvlOrdner gefunden", 1)
            #hier wär es möglich das DEFAULT-Level aus der levelCFG zu laden (nur müsste dazu die level.init zuerst überladen werden um ParameterObjekte anzunehmen)
        if(len(levels) == 0):
            DEBUG("KEINE LEVEL GEFUNDEN, TEMINIERE BATTLECASTLE", 0, LEVEL_DIR)
            self.error = True
#ToDo:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!HIER IS WAS FALSCH
    # erstellt einen Ladebildschirm und fügt in Mittig auf der PlayArea ein
    def set_loading_spinner(self, FilePath=DEFAULT_LOADING_SCREEN_PATH):
        self.isLoading = True
        pass

    # entfernt den LadeBildschirm, sofern aktiv
    # UNFERTIG
    def unset_loading_spinner(self):
        self.isLoading = False
        pass

    def load_loading_spinner(self, FilePath=""):
        if (os.path.exists(FilePath)):
            # UNFERTIG
            pass
        else:
            if (os.path.isfile(DEFAULT_LOADING_SPINNER_PATH)):
                spinner = pygame.image.load(DEFAULT_LOADING_SPINNER_PATH)
                return spinner

    # Zurückgestellt-----
    # def save(self):
    #    #In Zukunft sollen hier selbst erstellte Level gespeichert werden können
    #    pass

    # def create(self):
    #    #In Zukunft soll der Nutzer eigene Level erstellen können.
    #    #Da dies ein "NiceToHave"-Feature ist wird dies zunächst nicht implementiert
    #    pass
    # -----Zurückgestellt

    # WIRKLICH BENÖTIGT?:
    # gibt eine spriteGroup mit dem gesamten geladenen Level zurück
    def get_loaded_level(self):
        return self.loadedLevel

    def get_loaded_sprites(self):
        return self.allSprites


    def isColliding(self, object=pygame.sprite.sprite):
        return pygame.sprite.spritecollide(object, self.loadedLevel)

    def isColliding(self, object=pygame.sprite.group):
        return pygame.sprite.groupcollide(object, self.loadedLevel)


    def update(self):
    # animatedTiles gruppe updaten
        self.animatedTiles.update()
        # Playergruppe updaten
        self.players.update()
        self.draw()

    def draw(self, surface):
        self.allSprites.draw(surface)
        return surface

    def draw(self):
        self.allSprites.draw(self.image)
        self.rect = self.image.get_rect()
