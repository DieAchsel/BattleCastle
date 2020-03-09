# -*- coding: iso-8859-1 -*-
import pygame, glob, os, re
from bin.lib.Level import Level
from bin.lib.Tile import Tile
from bin.lib.Player import Player
from bin.config.levelCFG import LEVEL_DIR, DEFAULT_LOADING_SPINNER_PATH
from bin.config.generalCFG import *


# Das gesamte BattleCastle Game kann rheintheoretisch ein sprite sein, wodurch dem pygameDisplay nurnoch ein Objekt vom Typ BattleCastle übergeben wird und alles durch dessen updateMethode abläuft
class BattleCastle(pygame.sprite.Sprite):
    def __init__(self, rect=pygame.Rect(0,0,SCREEN_SIZE["X"],SCREEN_SIZE["Y"])):
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
        self.allSprites.add(self.players)
        self.isLoading = False
        self.load_levels()
        if(len(self.levels) > 0):
            self.activeLevel = len(self.levels) - 1
            self.levels[-1].build()
            self.allSprites.add(self.loadedLevel)


        self.allSprites.add(self.loadedLevel)
    # durchsucht das Level-Verzeichnis und erstellt für jeden gefundenen Ordner ein Level
    def load_levels(self):
        DEBUG("load_levels(self)", 0)
        DEBUG("lade Ladeanimation", 1)
        self.load_loading_spinner()  # Das Laden der Level könnte dauern
        DEBUG("suche nach Ordnern an Pfad", 2, LEVEL_DIR)
        lvlPaths = os.listdir(LEVEL_DIR)
        for path in lvlPaths:
            x = os.path.join(LEVEL_DIR, path)
            DEBUG("prüfe, ob angegebener Pfad ein Ordner ist", 3, x)
            if (not os.path.isdir(x)):
                DEBUG("angegebener Pfad ist kein Verzeichnis. Entferne Verzeichnis aus Liste", 3)
                lvlPaths.remove(path)
        if(len(lvlPaths) > 0):
            DEBUG("folgende Ordner wurden gefunden", 2, lvlPaths)
            for singlePath in lvlPaths:
                DEBUG("betrachte Ordner", 3, singlePath)
                #Wenn der betrachtete Ordner eine .lvl Datei enthält, dann erstelle ein neues Level
                #ist das so richtig mit path..join??

                lvlFileRegex = os.path.join(LEVEL_DIR, singlePath, '') + '*.lvl'
                DEBUG("suche nach .lvl Dateien mit: ", 4, lvlFileRegex)
                foundLvlFiles = glob.glob(lvlFileRegex)
                if(len(foundLvlFiles) > 0):
                    DEBUG("gefundene Lvl-Files ", 4, foundLvlFiles)
                    for lvlFile in foundLvlFiles:
                        DEBUG("erstelle Lvl und übergebe diesen Pfad Datei-Pfade ", 5, lvlFile)
                        self.levels.append(Level.Level(lvlFile))
                    self.activeLevel = 0
                else:
                    DEBUG("ES wurden keine LvlFiles gefunden", 4)
        else:
            DEBUG("ES wurden keine LvlOrdner gefunden", 2)
            self.error = True
            #hier wär es möglich das DEFAULT-Level aus der levelCFG zu laden (nur müsste dazu die level.init zuerst überladen werden um ParameterObjekte anzunehmen)
        if(len(self.levels) == 0):
            DEBUG("KEINE LEVEL GEFUNDEN, TEMINIERE BATTLECASTLE", 0, LEVEL_DIR)
            self.error = True

    # erstellt einen Ladebildschirm und fügt in Mittig auf der PlayArea ein
#    def set_loading_spinner(self, FilePath=DEFAULT_LOADING_SCREEN_PATH):
#        self.isLoading = True
#        pass

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


    def isColliding(self, object=pygame.sprite.Sprite()):
        return pygame.sprite.spritecollide(object, self.loadedLevel)

    def isColliding(self, object=pygame.sprite.Group()):
        return pygame.sprite.groupcollide(object, self.loadedLevel)


    def update(self):
    # animatedTiles gruppe updaten
        self.animatedTiles.update()
        # Playergruppe updaten
        self.players.update()

    def draw(self, surface):
        self.allSprites.draw(surface)
        return surface

#    def draw(self):
#        self.allSprites.draw(self.image)
#        self.rect = self.image.get_rect()
