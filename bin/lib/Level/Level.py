import pygame, os
from bin.lib.Level import Tile
from bin.config.levelCFG import *


#Lesen von Leveln muss noch implementiert werden
class Level:
    self.difficulty = 1
    self.name = "Level"
    self.gridSize = {"X": 0, "Y": 0}
    self.tilemap = []
    self.playerStartPositions = []
    self.textureList = []
    self.texture = {
        "textureSeq": [pygame.image],
        "id": 0,
        "Neighbors": [[0,0,0],
                      [0,1,0],
                      [0,0,0]]}


    def __init__(self):
        super().__init__()
    
    #Lese .lvl Datei
    def parseFile(self, FilePath = ""):
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

        else:
            print("kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?")
            rawLvl = DEFAULT_LVL
        return rawLvl

    #kompiliere Raster und sprites (noch ohne textur)
    def compile(self, rawLvl = DEFAULT_LVL):
        #baue die tileMap mit allen pygame.surfacebjekten (ohne geladenem image)
        pass

    #baue Level mit Texturen, entsprechend der Nachbarn
    def build(self):
        pass

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

    def set_grid(self, gridSize = DEFAULT_GRID_SIZE):


#Das kann noch nicht funktionieren, für jede textur muss erst den entsprechenden Slot mit der gleichen ID ermittelt werden und diesem Objekt die Textur angehängt werden
#Die Slots müssen noch beim parsen der rohen levelDaten angelegt werden, (nur die die für das level benutzt werden)
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
        