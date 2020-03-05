#nach Möglichkeit umbauen um eine dynamische Tileskalierung zu ermöglichen
#hierzu darf tile keine konstanten zur skalierung von tile verwenden
#stattdessen muss entweder die tilegröße woanders berechnet werden oder dem Konstruktor wird gridsize und screensize/areaSize übergeben

#Tiles können auch gut von StatusArea mitbenutzt werden
import pygame


from bin.config.levelCFG import *
from bin.config.generalCFG import COLORKEY, MISSING_TEXTURE_COLOR, SCALING, SMOOTH_SCALE, NULL_TYPE, DEBUG, AVAILABLE_IMG_FORMAT_REGEX, ANIMATION_INTERVAL
class Tile (pygame.sprite.Sprite):
    #skaliert imageObjekt auf eigene Tile-Größe
    def scale_texture(self, texture = pygame.image):
        if(SMOOTH_SCALE):
            return pygame.transform.smoothscale(texture, self.rect.w, self.rect.h)
        else:
            return pygame.transform.scale(texture, self.rect.w, self.rect.h)
    #wenn keine textur übergeben wird, wird das Objekt zunächst ohne textur erstellt
    def __init__(self, texturePath = "", newParameters = DEFAULT_TILE_CONF_PARAMETERS, newRect = pygame.Rect):
        super().__init__()
        DEBUG("Tile.init(self, texturePath = "", newParameters = DEFAULT_TILE_CONF_PARAMETERS, newRect = pygame.Rect)", 2)
        DEBUG("Tile.init(...): Lese parameter ein:", 2, newParameters)
        self.parameters = newParameters
        self.Name = newParameters["textureName"]
        self.layer = newParameters["layerID"]
        self.ID = newParameters["ID"]
        self.isclippable = newParameters["isclippable"]
        self.groupID = newParameters["groupID"]
        #self.isAnimated = newParameters["isAnimated"] #nicht benötigt, da dies von der images liste abhängt
        self.dmgNeededToDestroy = newParameters["dmgNeededToDestroy"]
        self.damageOnCollision = newParameters["damageOnCollision"]
        self.damageOverTime = newParameters["damageOverTime"]
        self.playMvSlowDown = newParameters["playMvSlowDown"]
        self.playerMvManipulation = newParameters["playerMvManipulation"]
        DEBUG("Tile.init(...): Lese rect(x,y,w,h) ein:", 2, newRect)
        self.rect = newRect
        self.imagesIndex = 0
        self.tick = 0
        self.images = []
        self.state = 0 #entspricht der Position im self.images dict (0 = passive, 1 = active, 2 = dying)
        DEBUG("Tile.init(...): Lade Texturen...", 2, texturePath)
        self.load_textures(texturePath)

    def load_textures(self, filePath = ""):
        DEBUG("Tile.load_textures(filePath = )", 1)
        tileTexturesPath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
        DEBUG("Tile.load_textures(...): betrachte Dateipfad", 2, tileTexturesPath)
        if(os.path.exists(tileTexturesPath) == False):
            DEBUG("Tile.load_textures(...): Dateipfad existiert nicht, versuche mit default TextureSet zu kombinieren", 1, DEFAULT_TEXTURE_SET_PATH)
            tileTexturesPath = DEFAULT_TEXTURE_SET_PATH
        if(os.path.exists(tileTexturesPath)):
            DEBUG("Tile.load_textures(...): suche in o.a. Dateipfad mit diesem Regex", 4, TEXTURE_DIVIDER_REGEX["all"] + AVAILABLE_IMG_FORMAT_REGEX)
            foundFiles = glob.glob(tileTexturesPath, TEXTURE_DIVIDER_REGEX["all"] + AVAILABLE_IMG_FORMAT_REGEX)
            DEBUG("Tile.load_textures(...): diese Dateien wurden gefunden:", 4, foundFiles) 
            
            regex = TEXTURE_DIVIDER_REGEX["passive"]
            regex.replace(REGEX_PLACEHOLDER, str(self.ID))
            foundFilePaths = glob.glob(tileTexturesPath, regex)
            self.images.append(list())
            for filePath in foundFilePaths:
                self.images[-1].append(self.scale_texture(pygame.image.load(filePath)).convert_alpha())

            regex = TEXTURE_DIVIDER_REGEX["active"]
            regex.replace(REGEX_PLACEHOLDER, str(self.ID))
            foundFilePaths = glob.glob(tileTexturesPath, regex)
            self.images.append(list())
            for filePath in foundFilePaths:
                self.images[-1].append(self.scale_texture(pygame.image.load(filePath)).convert_alpha())
            
            regex = TEXTURE_DIVIDER_REGEX["dying"]
            regex.replace(REGEX_PLACEHOLDER, str(self.ID))
            foundFilePaths = glob.glob(tileTexturesPath, regex)
            self.images.append(list())
            for filePath in foundFilePaths:
                self.images[-1].append(self.scale_texture(pygame.image.load(filePath)).convert_alpha())
                #alternative, falls Transparenzwerte nicht übernommen werden:        
                #im = pygame.Surface(self.rect.w, self.rect.h)
                #im.fill(COLORKEY, im.get_rect())
                #im.set_colorkey(COLORKEY)
                #im = self.scale_texture(pygame.image.load(filePath)).convert_alpha()
        else:#wenn kein Pfad (sowohl der lvlTexturpfad als auch der defaulttexturepfad) existiert
            DEBUG("Tile.load_textures(...): Default-Dateipfad existiert auch nicht, nutze einfarbiges Tile ohne textur", 1, DEFAULT_TEXTURE_SET_PATH)
            self.images.append(self.get_solid())
    #gibt ein einfarbiges image-Objekt mit den klasseneigenen tile dimensionen zurück# dient als Fallback, falls keine passende Textur geladen werden kann   
    def get_solid(self, rgb = MISSING_TEXTURE_COLOR):
        solid = pygame.Surface([self.rect.w, self.rect.h])
        solid.fill(rgb, solid.get_rect())
        solid.set_colorkey(COLORKEY)
        return solid
    #gibt true zurück, wenn mehr als 1 Bild geladen ist (wenn isActiveSequence = true, dann prüfe die ActiveSequence
    def has_animation(self, isActiveSequence = False):
        if(isActiveSequence):
            x = "active"
        else:
            x = "passive"
        if(len(self.images[x]) > 1):
            return True
        else:
            return False
    
    def has_collision(self):
        return self.isClippable
    
    def has_damage(self):
        return (self.damageOnCollision != 0 | self.damageOverTime != 0)
    
    def get_ID(self):
        return self.ID
    
    def get_group_ID(self):
        return self.groupID

    def get_state(self):
        return self.state

    def set_state(self, newState = 0):
        if(0 <= newState < len(self.images)):
            if(self.state != newState):
                self.state = newState
                self.index = 0                  #setze den index zurück
                self.tick = ANIMATION_INTERVAL #triggere einen bildWechsel
    
    def update(self): #Muss noch implementiert werden
        ANIMATION_INTERVAL
        self.tick += 1
        if(self.tick >= ANIMATION_INTERVAL):
            self.tick = 0
            self.index += 1
            if(self.index > len(images[state])):
                self.index = 0
            self.image = self.images[self.state][self.index]