import pygame


from bin.config.levelCFG import gridSize, arenaSize
from bin.config.generalCFG import COLORKEY, MISSING_TEXTURE_COLOR

class Tile (pygame.sprite.Sprite):
    tileSize = {"X": 64,
                "Y": 64}
    activeTexture = pygame.image
    passiveTextureSeq = [pygame.image]
    ActionTextureSeq = [pygame.image]
    damageOnCollision = 0   #negative Werte = heal
    damageOverTime = 0      #negative Werte = heal


    def scale_texture(self, texture = pygame.image):
        pass #skaliere übergebenes image Objekt auf tileSize

    def calc_tileSize(self):
        self.tileSize["X"] = gridSize["X"] // arenaSize["X"]
        self.tileSize["Y"] = gridSize["Y"] // arenaSize["Y"]

    def __init__(self, pos = {"X": 0, "Y": 0}, texture = pygame.image):
        super().__init__()
        calc_tileSize()

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


    def update(self): #Muss noch implementiert werden
        pass 
