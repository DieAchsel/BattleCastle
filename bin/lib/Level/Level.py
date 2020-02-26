import pygame


#fertig/muss noch getestet werden (speziell das texture Obj testen)
class Level:
    difficulty = 0
    name = ""
    id
    tilemap = []
    texture = {# hier komme ich etwas durcheinander mit den Datentypen: textureSeq soll eine Lise mit texturen beinhalten
    #texture selber soll wie ein struct (c++) agieren und nur diese 3 subtypen haben.
        "textureSeq": [pygame.image],
        "id": 0,
        "Neighbors": [[0,0,0],
                      [0,1,0],
                      [0,0,0]]}
    textureList = [texture]

    def __init__(self):
        super().__init__()

    def getID(self):
        return self.id

    def getTile(self, pos = {"X": 0, "Y": 0}):
        if(pos.X < self.tilemap.len & pos.Y < self.tilemap[pos.X].len):
            return self.tilemap[pos.X[pos.Y]]


    def setTile(self, pos = {"X": 0, "Y": 0}, type = 1):
        if(pos.X < self.tilemap.len & pos.Y < self.tilemap[pos.X].len):
            self.tilemap[pos.X[pos.Y]] = type

    def unsetTile(self, pos ={"X": 0, "Y": 0}):
        if(pos.X < self.tilemap.len & pos.Y < self.tilemap[pos.X].len):
            self.tilemap[pos.X[pos.Y]] = 0
    
    def getUsedTiles(self):
        used = []
        for x in tilemap:
            for y in x:
                if(y != 0):
                    used.add(y)
        return used

    def getUnusedTiles(self):
        unused = []
        for x in tilemap:
            for y in x:
                if(y == 0):
                    unused.add(y)
        return unused

    def setTextures(self, imObj, id, neighbors = [[0,0,0],
                                                  [0,1,0],
                                                  [0,0,0]]):
        temp = texture.copy()
        temp["TextureSeq"].add(imObj)
        temp["id"] = id
        temp["Neighbors"] = neighbors
        textureList.add(texture) #wird der textureSeqListe in texture so ein image übergeben?
        
    def getTextures(self):
        return texture["textureSeq"]
        