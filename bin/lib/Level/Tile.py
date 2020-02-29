#nach Möglichkeit umbauen um eine dynamische Tileskalierung zu ermöglichen
#hierzu darf tile keine konstanten zur skalierung von tile verwenden
#stattdessen muss entweder die tilegröße woanders berechnet werden oder dem Konstruktor wird gridsize und screensize/areaSize übergeben

#Tiles können auch gut von StatusArea mitbenutzt werden
import pygame


from bin.config.levelCFG import DEFAULT_GRID_SIZE, ARENA_SIZE, DEFAULT_LAYER_ID, DEFAULT_TILE_SIZE, DEFAULT_TILE_ID, DEFAULT_TEXTURE_SET_PATH, TILE_ID_RANGE_MAP
from bin.config.generalCFG import COLORKEY, MISSING_TEXTURE_COLOR, SMOOTH_SCALE

class Tile (pygame.sprite.Sprite):
    self.layer = DEFAULT_LAYER_ID
    self.ID = DEFAULT_TILE_ID
    self.tileSize = {
        "X": DEFAULT_TILE_SIZE,
        "Y": DEFAULT_TILE_SIZE}
    self.activeTexture = pygame.image
    self.passiveTextureSeq = [pygame.image]
    self.ActionTextureSeq = [pygame.image]


    #Diese Funktion am besten in den Levelmanager verschieben und tile über den init die Größe von extern beziehen
    #wenn keine größe übergeben, dann grösse der Textur übernehmen
    #dient unteranderem dazu die obtimale Feldgröße des StatusArea-raster zu ermitteln
    def scale_texture(self, texture = pygame.image):
        if(SMOOTH_SCALE):
            return pygame.transform.smoothscale(texture, self.tileSize["X"], self.tileSize["Y"])
        else:
            return pygame.transform.scale(texture, self.tileSize["X"], self.tileSize["Y"])

    def calc_tileSize(self, gridSize = DEFAULT_GRID_SIZE):
        self.tileSize["X"] = gridSize["X"] // ARENA_AREA.w
        self.tileSize["Y"] = gridSize["Y"] // ARENA_AREA.h

    def __init__(self, pos = {"X": 0, "Y": 0}, texturePath = "DEFAULT_TEXTURE_SET_PATH"):
        super().__init__()
        calc_tileSize()
        
        if( TILE_ID_RANGE_MAP["uncollidable"]["first"] <= self.ID <= TILE_ID_RANGE_MAP["collidable"]["last"]):
            self.damageOnCollision = 0   #negative Werte = heal
            self.damageOverTime = 0      #negative Werte = heal
        elif(self.ID):
            

            

        self.image = pygame.Surface([self.tileSize["X"],self.tileSize["Y"]])
        self.rect = self.image.get_rect()
        self.image.fill(COLORKEY, self.image.get_rect())
        self.image.set_colorkey(COLORKEY)

        self.image.blit(texture.convert(), self.image.get_rect)
        self.activeTexture = self.image

    def __init__(self, newRect = pygame.Rect, texture = [pygame.image]):
        super().__init__()

        calc_tileSize()

        self.image = pygame.Surface([self.tileSize["X"],self.tileSize["Y"]])
        self.rect = self.image.get_rect()
        
        self.image.set_colorkey(COLORKEY)
        if(len(texture) > 0):
            #skaliere jede Textur in der Liste auf die tileMaße und setze den Hintergrund entsprechend COLORKEY
            for x in texture:
                self.image.fill(COLORKEY, self.image.get_rect())
                self.image.blit(x.convert(), self.image.get_rect())
                self.passiveTextureSeq.append(self.image)
            self.hasAnimation = True
        else:
            self.image.fill(MISSING_TEXTURE_COLOR, self.image.get_rect())
            self.hasAnimation = False

        self.hasAction = False
        self.activeTexture = self.image
        
    def __init__(self, newRect = pygame.Rect, texture = pygame.image, actionTexture = pygame.image):
        super().__init__()

        calc_tileSize()

        self.image = pygame.Surface([self.tileSize["X"],self.tileSize["Y"]])
        self.rect = self.image.get_rect()

        self.image.fill(COLORKEY, self.image.get_rect())
        self.image.set_colorkey(COLORKEY)

        self.image.blit(actionTexture.convert(), self.image.get_rect)
        self.activeTextureSeq.append(self.image)

        self.image.fill(COLORKEY, self.image.get_rect())
        self.image.blit(texture.convert(), self.image.get_rect)
        self.passiveTextureSeq.append(self.image)
        self.activeTexture = self.image
        self.hasAnimation = False
        self.hasAction = True

    def __init__(self, newRect = pygame.Rect, texture = [pygame.image], actionTexture = [pygame.image]):
        super().__init__()

        calc_tileSize()

        self.image = pygame.Surface([self.tileSize["X"],self.tileSize["Y"]])
        self.rect = self.image.get_rect()
        
        self.image.set_colorkey(COLORKEY)
        if(len(actionTexture) > 0):
            #skaliere jede Textur in der Liste auf die tileMaße und setze den Hintergrund entsprechend COLORKEY
            for x in actionTexture:
                self.image.fill(COLORKEY, self.image.get_rect())
                self.image.blit(x.convert(), self.image.get_rect())
                self.actionTextureSeq.append(self.image)
            self.hasAction = True
        else:
             hasAction = False
        if(len(texture) > 0):
            for x in texture:
                self.image.fill(COLORKEY, self.image.get_rect())
                self.image.blit(x.convert(), self.image.get_rect())
                self.textureSeq.append(self.image)
            self.activeTexture = self.image
            self.hasAnimation = True
        else:
            self.image.fill(MISSING_TEXTURE_COLOR, self.image.get_rect())
            self.activeTexture = self.image
            self.hasAnimation = False
        

        


    def has_animation(self):
        return self.hasAnimation

    def has_action(self):
        return self.hasAction

    def getTexture(self):
        return self.activeTexture

    def getTextureSeq(self):
        return self.passiveTextureSeq
    def get_type(self)

    def update(self): #Muss noch implementiert werden
        pass 
