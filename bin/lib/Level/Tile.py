import pygame


from bin.config.levelCFG import DEFAULT_GRID_SIZE, ARENA_SIZE, DEFAULT_LAYER_ID, DEFAULT_TILE_SIZE
from bin.config.generalCFG import COLORKEY, MISSING_TEXTURE_COLOR, SMOOTH_SCALE

class Tile (pygame.sprite.Sprite):
    self.layer = DEFAULT_LAYER_ID
    self.tileSize = {
        "X": DEFAULT_TILE_SIZE,
        "Y": DEFAULT_TILE_SIZE}
    self.activeTexture = pygame.image
    self.passiveTextureSeq = [pygame.image]
    self.ActionTextureSeq = [pygame.image]
    self.damageOnCollision = 0   #negative Werte = heal
    self.damageOverTime = 0      #negative Werte = heal


    def scale_texture(self, texture = pygame.image):
        if(SMOOTH_SCALE):
            return pygame.transform.smoothscale(texture, self.tileSize["X"], self.tileSize["Y"])
        else:
            return pygame.transform.scale(texture, self.tileSize["X"], self.tileSize["Y"])

        

#Anpassung notwendig!! TileSize richtet sich nach der gridSize im geladenen Level
    def calc_tileSize(self, gridSize = DEFAULT_GRID_SIZE):
        self.tileSize["X"] = gridSize["X"] // ARENA_SIZE["X"]
        self.tileSize["Y"] = gridSize["Y"] // ARENA_SIZE["Y"]

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
