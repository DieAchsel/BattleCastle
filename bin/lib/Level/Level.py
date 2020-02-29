import pygame, os
from bin.lib.Level import Tile
from bin.config.levelCFG import *


#Lesen von Leveln muss noch implementiert werden
class Level:
    self.difficulty = DEFAULT_DIFFICULTY
    self.title = "Level"
    self.gridSize = pygame.rect(0, 0, 0, 0) #zu kompatiblität ein rect. X und Y werden nicht mit einbezogen (vllt später als Position in der Arena?)
    self.currentTile = {"X": 0, "Y": 0} # gibt an, welche tilePosition grade betrachtet wird
    self.tilemap = []
    self.playerStartPositions = DEFAULT_PLAYER_STARTPOS
    self.loadedTileIDs = [
        {
            "ID": 0, #TileID
            "Parameters": DEFAULT_TILE_CONF_PARAMETERS #zugehöriges ausgelesenes ParameterDict
        }
    ]

    self.textureList = [] #DEPRECATED (to be removed)
    self.texture = {    #DEPRECATED (to be removed)
        "textureSeq": [pygame.image],
        "id": 0,
        "Neighbors": [[0,0,0],
                      [0,1,0],
                      [0,0,0]]}


    def __init__(self):
        super().__init__()
        self.difficulty = DEFAULT_LVL["difficulty"]
        self.name = DEFAULT_LVL["title"]
        self.tilemap = DEFAULT_LVL["grid"]
    def __init__(self, FilePath = ""):
        super().__init__()
        if(FilePath != ""):
            self.parseLvl(FilePath)
    #Lese .lvl Datei
    def parseLvl(self, FilePath = ""):
        self.playerStartPositions = DEFAULT_PLAYER_STARTPOS.copy()
        if(os.path.isFile(FilePath)): #datei vorhanden?
                lvlFile = open(FilePath, "r")
                if(len(lvlFile) > 0): #inhalt nicht leer?
                    lvlData = lvlData.replace(" ", "")
                    rawLvl = DEFAULT_LVL.copy()
                    rawLvl["grid"].clear()
                    for line in lvlFile:
                        for conditionName in DATA_CONDITIONS:
                            condition = DATA_CONDITIONS[conditionName]
                            results = re.search(condition, line)    #hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                            if(results[-1] != 'none'): 
                                if conditionName == "grid":
                                    for x in results:
                                        tileTypeList = x.split(';')
                                        if(len(tileTypeList) > rawLvl["maxWidth"]):
                                            rawLvl["maxWidth"] = len(tileTypeList)   
                                        rawLvl["grid"].add(list(map(int, tileTypeList))) #wandelt String-liste in int-liste um und fügt sie der tilemap zu
                                elif conditionName == "difficulty":
                                    extractedDifficulties = list(map(int, results.replace("difficulty=", "")))
                                    rawLvl["difficulty"] = extractedDifficulties[-1]
                                elif conditionName == "playerStartPos":
                                    self.playerStartPositions.clear()
                                    extractedplayerStartPositions = list(map(int, results.replace("playerStartPos=", "")))
                                    startPosList = extractedplayerStartPositions[-1].split(')(')
                                    for x in startPosList:
                                        self.playerStartPositions = list(map(int, x.replace("(", "").replace(")", "").split(';') ))
                            re.purge() #re-Chache leeren
                else: 
                    print("kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level")
                    rawLvl = DEFAULT_LVL
                    self.gridSize = (0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"]) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird

        else:
            print("kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?")
            rawLvl = DEFAULT_LVL
            self.gridSize = (0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"]) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird
        self.difficulty = rawLvl["difficulty"]
        self.title = rawLvl["title"]
        self.tilemap = rawLvl["grid"]
        
    #lade und parse textureSetConf
    def parseTextureSet(self, FilePath = ""):

        tileObject = DEFAULT_TILE_CONF_PARAMETERS.copy()
        #ausgelesene ID Objekt in tileObjet parsen und self.loadedTileIDs hinzufügen
        #
        pass

#gibt die NachbarTiles der übergebenen Position zurück, wenn es ein äußeres Tile ist, dann nutze die RandTiles von der gegenüberliegende Seite mit, sodass ein endlosbildschirm entsteht
    def getNeighbors(self, position = {"X": 0, "Y": 0}):
        return neigbhors
    
    #1. lade textureSetConf und beschreibe sämtliche geladenen Tiles mit den zu GroupID entsprechenden Eigenschaften
    #2. wähle im 2. Schritt die passende TileID(entsprechend der Neighbors) aus der geöffneten Gruppe aus
    #3. erstelle ein tile und übergebe den texturepfad des entsprechenden tiles
    #das bild wird erst mit build() geladen um zu verhindern dass alle lvl parallel offen sind
    def compileLvl(self, path = "DEFAULT_TEXTURE_SET_PATH"):



    #ersetze sämtlichen tileTypeIDs mit entsprechenden Texturen (pygame.image Objekte)
    #erstelle eine sprite.group mit sämtlichen tiles, passiven tiles, animierten tiles, 
    #wenn IS_BUILD_ON_UPDATE = True, dann wird mit jedem build aufruf nur ein tile verändert und currentTile auf dieses gesetzt

    def build(self):
        pass
    
    #wenn das level wechselt, setze die tiles zurück auf
    #das geladene Bild wird durch eine solide Farbe ersetzt, oder das imageObjekt wird sogar zerstört
    def unbuild(self):
        for line in self.tilemap:
            for field in line:
                field = field.get_type()

    def tile_exists(self, pos = {"X": 0, "Y": 0}):
        return (0 <= pos["X"] < len(self.tilemap) & 0 <= pos["Y"] < len(self.tilemap[pos["X"]]))

    def get_tile_type(self, pos = {"X": 0, "Y": 0}):


    def get_ID(self):
        return self.id

    def get_tile(self, pos = {"X": 0, "Y": 0}):
        if(field_exist(pos)):
            return self.tilemap[pos.X[pos.Y]]

    def set_tile(self, pos = {"X": 0, "Y": 0}, type = 1):
        if(field_exist(pos)):
            self.tilemap[pos["X"][pos["Y"]]] = type

    def unset_tile(self, pos ={"X": 0, "Y": 0}):
        if(field_exist(pos)):
            self.tilemap[pos.X[pos.Y]] = 0
    
    def get_used_tiles(self):
        used = []
        for x in self.tilemap:
            for y in x:
                if(y != 0):
                    used.add(y)
        return used

    def get_unused_tiles(self):
        unused = []
        for x in self.tilemap:
            for y in x:
                if(y == 0):
                    unused.add(y)
        return unused


#Das kann noch nicht funktionieren, für jede textur muss erst den entsprechenden Slot mit der gleichen ID ermittelt werden und diesem Objekt die Textur angehängt werden
#Die Slots müssen noch beim parsen der rohen levelDaten angelegt werden, (nur die die für das level benutzt werden)
#-----DEPRECATED(to be removed)
    def add_texture(self, imObj, id, neighbors = [[0,0,0],
                                                  [0,1,0],
                                                  [0,0,0]]):
        temp = self.texture.copy()
        temp["TextureSeq"].add(imObj)
        temp["id"] = id
        if(len(neighbors) == 3 & len(neighbors[0]) == 3 & len(neighbors[1]) == 3 & len(neighbors[2]) == 3):
            temp["Neighbors"] = neighbors
        self.textureList.add(temp) #wird der textureSeqListe in texture so ein image übergeben?
        
    def get_textures(self):
        return self.textureList
#-----DEPRECATED(to be removed)