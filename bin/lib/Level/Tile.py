#nach Möglichkeit umbauen um eine dynamische Tileskalierung zu ermöglichen
#hierzu darf tile keine konstanten zur skalierung von tile verwenden
#stattdessen muss entweder die tilegröße woanders berechnet werden oder dem Konstruktor wird gridsize und screensize/areaSize übergeben

#Tiles können auch gut von StatusArea mitbenutzt werden
import pygame


from bin.config.levelCFG import *
from bin.config.generalCFG import COLORKEY, MISSING_TEXTURE_COLOR, SCALING, SMOOTH_SCALE, NULL_TYPE
class Tile (pygame.sprite.Sprite):
    self.layer = DEFAULT_LAYER_ID
    self.ID = DEFAULT_TILE_ID
    self.isclippable = False
    self.groupID = DEFAULT_TILE_GROUP_ID
    self.tileSize = {
        "X": DEFAULT_TILE_SIZE,
        "Y": DEFAULT_TILE_SIZE}
    self.textureSequences = {
        "passive": [],
        "active": []
    }


    #skaliert imageObjekt auf eigene Tile-Größe
    def scale_texture(self, texture = pygame.image):
        if(SMOOTH_SCALE):
            return pygame.transform.smoothscale(texture, self.tileSize["X"], self.tileSize["Y"])
        else:
            return pygame.transform.scale(texture, self.tileSize["X"], self.tileSize["Y"])

    #berechnet die tileSize anhand der größe der Arena und der übergenebenen Anzahl der tiles in X und Y richtung
    def calc_tileSize(self, gridSize = {}):
        if(len(gridSize == 2)):
            self.tileSize["X"] = gridSize["X"] // ARENA_AREA.w
            self.tileSize["Y"] = gridSize["Y"] // ARENA_AREA.h
        else:
            self.tileSize = DEFAULT_TILE_SIZE

    #erstellt ein tileObjekt. 
    #wenn keine textur übergeben wird, wird das Objekt zunächst ohne textur erstellt
    def __init__(self, pos = {"X": 0, "Y": 0}, texturePath = "", parameters = DEFAULT_TILE_CONF_PARAMETERS, gridSize = {}):
        super().__init__()

        calc_tileSize(gridSize)#berechne tileSize anhand der lvlgröße
        self.image = pygame.Surface([self.tileSize["X"],self.tileSize["Y"]])
        self.rect = self.image.get_rect()
        self.image.fill(COLORKEY, self.image.get_rect())
        self.image.set_colorkey(COLORKEY)
        self.add_texture(texturePath)

    #fügt eine Textur hinzu, über die Flag isActive kann die übergebene Textur zusätzlich als aktive texture markiert werden
    def add_texture(self, FilePath = "", isActiveTexture = False):
        texture = pygame.image()
        if(os.path.isfile(FilePath)):
            texture = pygame.image.load(FilePath)
            if(SCALING):
                texture = self.scale_texture(texture) #passe Textur auf tilegröße an
        else:
            #Falle hier in Zukunft auf eine benachbarte Textur oder auf StandardTexturen zurück
            texture = pygame.image.fill(MISSING_TEXTURE_COLOR, self.image.get_rect())
        if(isActiveTexture):
            self.textureSequences["active"].add(texture)
        else:
            self.textureSequences["passive"].add(texture)
        #self.image.blit(texture.convert(), self.image.get_rect)
        #self.activeTexture = self.image

    #gibt true zurück, wenn mehr als 1 Bild geladen ist (wenn isActiveSequence = true, dann prüfe die ActiveSequence
    def has_animation(self, isActiveSequence = False):
        if(isActiveSequence):
            x = "active"
        else:
            x = "passive"
        if(len(self.textureSequences[x]) > 1):
            return True
        else:
            return False

    def has_action(self):
        return self.hasAction

    def getTexture(self):
        return self.activeTexture

    def getTextureSeq(self):
        return self.passiveTextureSeq
    def get_ID(self):
        return self.ID
    def get_group_ID(self):
        return self.groupID
    def update(self): #Muss noch implementiert werden
        pass 
