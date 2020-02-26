import pygame


#fertig/muss noch getestet werden (speziell das texture Obj testen)
class Level:
    self.difficulty = 1
    self.name = "Level"
    self.tilemap = []

    #texture selber soll wie ein struct (c++) agieren und nur diese 3 subtypen haben.
    #hier komme ich etwas durcheinander mit den Datentypen: textureSeq soll eine Lise mit texturen beinhalten
    self.texture = {
        "textureSeq": [pygame.image],
        "id": 0,
        "Neighbors": [[0,0,0],
                      [0,1,0],
                      [0,0,0]]}
    
    self.textureList = []

    def __init__(self):
        super().__init__()

    def field_exist(self, pos = {"X": 0, "Y": 0}):
        return (0 <= pos["X"] < len(self.tilemap) & 0 <= pos["Y"] < len(self.tilemap[pos["X"]]))

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

    def set_textures(self, imObj, id, neighbors = [[0,0,0],
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
        