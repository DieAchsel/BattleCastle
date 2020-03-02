import pygame, os
from bin.lib.Tile import Tile
from bin.config.generalCFG import NULL_TYPE, DEBUG
from bin.config.levelCFG import *


#Lesen von Leveln muss noch implementiert werden
class Level:

#---------------------------------------Klassen-Variablen--------------------------------------------------
    self.parameters = {
        "title" : "Level",
        "levelFilePath" : "", #UNUSED #Datei-Pfad zu Ordner, der 
        "difficulty" : DEFAULT_DIFFICULTY,
        "playerStartPositions" : DEFAULT_PLAYER_STARTPOS
    }
    
    self.title = "Level"
    self.levelDir = "" #UNUSED #Datei-Pfad zu Ordner, der 
    self.difficulty = DEFAULT_DIFFICULTY
    self.playerStartPositions = DEFAULT_PLAYER_STARTPOS
    self.gridSize = pygame.rect(0, 0, 0, 0) #zu kompatiblität ein rect. X und Y werden nicht mit einbezogen (vllt später als Position in der Arena?)
    self.currentTile = {"X": 0, "Y": 0} # gibt an, welche tilePosition grade betrachtet wird
    
    #diese 2D Liste wird zur Datenhaltung beim parsen und kompilieren des LevelFiles genutzt
    self.tileIDMap = [list()]
    #diese (zukünftige) 2D Liste wird zu Datenhaltung beim build genutzt (ggfs später unnötig, da build() bereits die zur Spielzeit benötgten spritegruppen erstellt)
    self.tileSurfaceMap = [] #DEPRECATED (beim buildVorgang erstellte Tiles werden direkt in die spriteListe eingefügt)
    loadedTiles = pygame.sprite.Group
    #Zustands-Indikatoren für Level
    #Das level muss alle 3 Phasen nacheinander durchlaufen, um gefüllte SpriteGroups zu besitzen
    self.isMapParsed = False
    self.isMapCompiled = False
    self.isMapBuild = False
    
    

    #jede geladene tile aus dem TileSet wird hierein geparst und geladen
    self.loadedTiles = [
        {
            "ID": 0, #TileID
            "Parameters": DEFAULT_TILE_CONF_PARAMETERS, #zugehöriges ausgelesenes ParameterDict
            "textureName": "000" # Dateipfad zu entsprechender Textur (die untertexturen 000[_; -; #]0, 000[_; -; #]1, etc. werden aus diesem Namen bestimmt und per regex gesucht)
        }
    ]

    self.textureList = [] #DEPRECATED (to be removed)
    self.texture = {    #DEPRECATED (to be removed)
        "textureSeq": [pygame.image],
        "id": 0,
        "Neighbors": [[0,0,0],
                      [0,1,0],
                      [0,0,0]]}


#---------------------------------------Klassen-Methoden--------------------------------------------------

    #konstruktor, ruft parse auf
    def __init__(self, levelFilePath = NULL_TYPE):
        DEBUG("Level.__init__(lvlDir = NULL_TYPE)", 0)
        DEBUG("Level.__init__:übergebener filePath",1 , levelFilePath)
        super().__init__()
        DEBUG("Level.__init__(lvlDir = NULL_TYPE): rufe Level.compile(filePath) auf", 1)
        if(os.path.isFile(levelFilePath) == False):
            #hier gäb es die Möglichkeit eine Suche ausgehend von übergebenem Pfad anstoßen und nach einem Ordner im übergelegenen Verzeichnis suchen
            DEBUG("Level.__init__(lvlDir = NULL_TYPE): Level-Directory nicht gefunden, überlasse das Problem den folgenden build-Prozess...", 0)
        self.compile(levelFilePath)
        DEBUG("Level.__init__(lvlDir = NULL_TYPE): Init abgeschlossen", 1)
    

    #gibt die NachbarTiles der übergebenen Position zurück, wenn es ein äußeres Tile ist, dann nutze die RandTiles von der gegenüberliegende Seite mit, sodass ein endlosbildschirm entsteht
    def get_neighbors(self, position = {"X": 0, "Y": 0}):
        DEBUG("Level.get_neighbors(position{})", 1, position)
        #ändere Position auf den oben linken nachbarn
        position["X"] -= 1
        position["Y"] -= 1
        currentNeighbor = position.copy() #erstelle ein identisches dict zu position
        neighbors = []
        #gehe Alle 3 möglichen NachbarZeilen durch
        for y in range(3):
            
            #füge eine neue Y Liste hinzu
            neighbors.add(list())
            currentNeighbor["Y"] = position["Y"].copy()
            currentNeighbor["Y"] += y
            DEBUG("Level.get_neighbors(position{}) wähle Y Position: " + currentNeighbor["Y"] , 3)
            #wenn Nachbar nicht vorhanden (Rand)
            #dann nehme entsrechenden randtile von der gegenüberliegenden Seite als nachbarn
            #erstellt eine von den tiles her eine endlos-Arena
            if(currentNeighbor["Y"] < 0):
                currentNeighbor["Y"] = (len(self.tileIDMap) - 1)
                DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + currentNeighbor["Y"] + "als Nachbarn", 4)
            elif(currentNeighbor["Y"] >= (len(self.tileIDMap))):
                currentNeighbor["Y"] = 0
                DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + currentNeighbor["Y"] + "als Nachbarn", 4)
            #wiederhole obiges für jedes Feld in aktueller Zeile
            for x in range (3):
                neighbors[-1].add(list())
                currentNeighbor["X"] = position["X"].copy() #currentNeighbor wird nach durchlauf manipuliert sein, setze current Neighbor zurück auf position(erste NachbarPos ecke oben links)
                currentNeighbor["X"] += x
                DEBUG("Level.get_neighbors(position{}) wähle X Position: " + currentNeighbor["X"] , 3)
                if(currentNeighbor["X"] < 0):
                    currentNeighbor["X"] = (len(self.tileIDMap[position["Y"]]) - 1)
                    DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + currentNeighbor["X"] + "als Nachbarn", 4)
                elif(currentNeighbor["X"] == (len(self.tileIDMap))):
                    currentNeighbor["X"] = 0
                    DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + currentNeighbor["X"] + "als Nachbarn", 4)
                neighbors[y][x] = self.get_tile_ID(currentNeighbor)
        DEBUG("Level.get_neighbors(position{}) abgeschlossen", 2, neighbors)
        return neighbors
    
    #Lese .lvl Datei (debugging implementiert)
    def parse_lvl_file(self, filePath = ""):
        DEBUG("Level.parse_lvl_file(lvlDir)", 0)
        DEBUG("Level.parse_lvl_file: übergebener DateiPfad",1, filePath)
        self.playerStartPositions = DEFAULT_PLAYER_STARTPOS.copy()
            #optimierbar: erstellle für jede gefundene Datei ein unterlevel
        if(os.path.isFile(filePath)): #datei vorhanden?
                lvlFile = open(filePath, "r")
                DEBUG("Level.parse_lvl_file: Datei geöffnet:\n", 1) 
                DEBUG("Level.parse_lvl_file: DateiInhalt: ", 2, lvlFile)                  
                if(len(lvlFile) > 0): #inhalt nicht leer?
                    lvlData = lvlFile.replace(" ", "")
                    DEBUG("Level.parse_lvl_file: Datei getrimmt:\n", 2, lvlData)
                    rawLvl = DEFAULT_LVL.copy()
                    rawLvl["grid"].clear()
                    for line in lvlData:
                        DEBUG("Level.parse_lvl_file: parse Zeile:\n", 2, line)
                        for conditionName in DATA_CONDITIONS:
                            condition = DATA_CONDITIONS[conditionName]
                            DEBUG("Level.parse_lvl_file: nutze Zur Suche von" + conditionName + " diesen RegEx-Ausdruck: ", 3, condition)
                            results = re.search(condition, line)    #hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                            DEBUG("Level.parse_lvl_file: " + len(results) + "gefundene Zeile(n):\n", 5, results)
                            if(results[-1] != 'none'): 
                                if conditionName == "grid":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " grid Zeilen gefunden" , 4)
                                    for x in results:
                                        tileTypeCols = x.split(';')

                                        DEBUG("Level.parse_lvl_file: " + len(tileTypeCols) + " grid Spalten in dieser zeile gefunden", 5 , x)

                                        if(len(tileTypeCols) > rawLvl["maxWidth"]):
                                            rawLvl["maxWidth"] = len(tileTypeCols)   
                                            DEBUG("Level.parse_lvl_file: längste Spalte gefunden, Tilemap hat jetzt " + rawLvl["maxWidth"] + " Spalten", 5)
                                        rawLvl["grid"].add(list(map(int, tileTypeCols))) #wandelt String-liste in int-liste um und fügt sie der tileIDMap zu
                                elif conditionName == "difficulty":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " difficulty Paramter gefunden, wähle: " , 4, results[-1])
                                    extractedDifficulties = list(map(int, results.replace("difficulty=", "")))
                                    rawLvl["difficulty"] = extractedDifficulties[-1]
                                    
                                elif conditionName == "playerStartPos":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " playerStartPos Paramter gefunden, wähle: " , 4, results[-1])
                                    self.playerStartPositions.clear()
                                    extractedplayerStartPositions = list(map(int, results.replace("playerStartPos=", "")))
                                    startPosList = extractedplayerStartPositions[-1].split(')(')
                                    for x in startPosList:
                                        DEBUG("Level.parse_lvl_file: füge (" + len(results) + " difficulty Paramter gefunden, wähle: " , 5, results[-1])

                                        #hier muss noch was gemacht werden! in der playerStartPos liste sind yPositionen nur an der ungeraden ID erkennbar
                                        self.playerStartPositions = list(map(int, x.replace("(", "").replace(")", "").split(';') ))
                            DEBUG("Level.parse_lvl_file: Zeile Abgeschlossen" , 3)
                            re.purge() #re-Chache leeren
                else: 
                    DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level", 1)
                    rawLvl = DEFAULT_LVL
                    self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird

        else:
            DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?", 1)
            rawLvl = DEFAULT_LVL
            
            self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird
        self.difficulty = rawLvl["difficulty"]
        self.title = rawLvl["title"]
        self.tileIDMap = rawLvl["grid"]
        self.gridSize = (0,0, (rawLvl["maxWidth"], len(self.tileIDMap)))
        DEBUG("Level.parse_lvl_file: nutze zum konfigurieren diese Werte: " , 0, rawLvl)



    #finde, lade und parse textureSetConf-File im übergebenen Verzeichnis in loadedTiles hinein
    def parse_texture_set(self):
        DEBUG("Level.parse_texture_set(levelPath)", 0)
        tileObject = self.loadedTiles[-1].copy()
        self.loadedTile.clear()
        #baue den Pfad für parse_texture_set
        textureSetPath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture")
        if(os.path.isdir(textureSetPath) == False):
            DEBUG("Level.parse_texture_set(levelPath): TexturPfad nicht gefunden. falle auf DefaultTexturSet zurück...", 0, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
        foundConfFilePaths = glob.blod(os.path.join(textureSetPath, '') + '*.conf')
        if(len(foundConfFilePaths) == 0):
            DEBUG("Level.parse_texture_set(levelPath): TexturPfad enthält keine Textur Datei/en(.conf). falle auf DefaultTexturSet zurück...", 0, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
        #für jeden gefundenden .confFile ließ alle enthaltenen ParameterObjekte ein
        #finde alle conf dateien
        #gehe alle durch und appende die tileID liste (suche vor jedem Eintrag erst ob es deisen bereits gibt)
        #durchsuche .conf Datei mit regex nach Parametern wie bei parse_lvl_file
        #nutze dabei die in TILE_CONF_REGEX enthaltenen RegEx Ausdrücke um jedes Objekt zu finden
        for confFilePath in foundConfFilePaths: 
            confFile = open(confFilePath, "r")
            if(len(confFile) > 0): #inhalt nicht leer?
                confData = confFile.replace(" ", "")
                DEBUG("Level.parse_texture_set: Datei getrimmt:\n", 2, confData)
                rawParameters = loadedTiles[0].copy()   
                loadedTiles.clear() #loadedTiles vorbereiten für einzufügende TileIDs

                for line in confData:
                    DEBUG("Level.parse_texture_set: parse Zeile:\n", 2, line)
                    condition = TILE_CONF_REGEX["ID"]
                    DEBUG("Level.parse_texture_set: nutze Zur Suche von ID-Blöcken diesen RegEx-Ausdruck: ", 3, condition)
                    #ich brauche einen anderen RegEx Ausdruck... (Idee ist es die gesamte Datei in einen String zusammenzufassen und de komplette Datei in einem zu scannen nach ID:\d+\{irgendwas*})
                    results = re.search(condition, line)    #hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                    DEBUG("Level.parse_texture_set: " + str(len(results)) + "gefundene ID-Blöcke:\n", 4, results)
                    if(results[-1] != 'none'): 
                        for x in results:
 #<-----------------------       #hier mit regex die ID-Blöcke durchgehen 1 Block steht mit jedem Durchlauf in x         
                            pass
                    re.purge() #re-Chache leeren
            else: 
                DEBUG("Level.parse_texture_set: kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level", 1)





    #1. lade textureSetConf und beschreibe sämtliche geladenen Tiles mit den zu GroupID entsprechenden Eigenschaften
    #2. wähle im 2. Schritt die passende TileID(entsprechend der Neighbors) aus der geöffneten Gruppe aus
    #3. erstelle ein tile und übergebe den texturepfad des entsprechenden tiles
    #das bild wird erst mit build() geladen um zu verhindern dass alle lvl parallel offen sind
    def compile_lvl(self):
        DEBUG("Level.compile()", 0)
        DEBUG("Level.compile(): rufe parse_lvl_file() auf", 1)
        self.parse_lvl_file()
        self.parse_texture_set()
    #1. ließt alle tileIDs ein und lädt jewils die entsprechende textur
    #2. erstelle eine sprite.group mit sämtlichen tiles, passiven tiles, animierten tiles, 
    #wenn IS_BUILD_ON_UPDATE = True, dann wird mit jedem build aufruf nur ein tile erstellt und currentTile auf dieses gesetzt. 
    #(überprüfen lässt sich der aktuelle Build-Zustand mit bool self.isBuild())
    def build(self):
        if(IS_BUILD_ON_UPDATE):
            loadedTiles.add(load())
            if(self.currentTile["X"] < self.gridSize.w): #wenn XPos noch in der Arena
            if(self.currentTile["Y"] < self.gridSize.h) 
#<-----------------
        else:

    #lädt ein tile an angegebener Stelle aus dem Speicher und gibt ein imageObjekt zurück
    def load(self, position = self.currentTile):
        pass
    #leert sämtliche Spritegruppen und zerstört dessen Tiles (Schafft platz im RAM)
    def unload_all(self):

        pass
    #führe ein unload() aus und lade erneut mit load()
    def reload(self):
        self.unload()
        self.load()





    #wenn das level wechselt, setze die tiles zurück auf
    #das geladene Bild wird durch eine solide Farbe ersetzt, oder das imageObjekt wird sogar zerstört
    #DEPRECATED----- (wird von unload() übernommen)
    def unbuild(self):
        self.tileSurfaceMap.clear()
    #-----DEPRECATED
    def tile_exists(self, pos = {"X": 0, "Y": 0}):
        return (0 <= pos["Y"] < len(self.tileIDMap) & 0 <= pos["X"] < len(self.tileIDMap[pos["Y"]]))

    def get_tile_ID(self, pos = {"X": 0, "Y": 0}):
        if(self.get_tile_surface(pos).getType() == NULL_TYPE):
            return NULL_TYPE
        else:
            self.get_tile_surface(pos).getType()
    #gibt
    def get_ID(self):
        return self.id

    #DEPRECATED-----
    #gibt die Oberfläche an pos zurück
    def get_tile_surface(self, pos = {"X": 0, "Y": 0}):
        if(self.tile_exists(pos)):
            return self.tileSurfaceMap[pos.X][pos.Y]
        else: 
            return NULL_TYPE
    #DEPRECATED-----

    #ändert tile in tileIDMap auf übergebenen ID
    def set_tile(self, pos = {"X": 0, "Y": 0}, ID = 1):
        if(tile_exists(pos)):
            self.tileIDMap[pos["X"]][pos["Y"]] = ID
            return pos
        else:
            return NULL_TYPE






    #muss noch lernen tile-Objekte zu verarbeiten
    def unset_tile(self, pos ={"X": 0, "Y": 0}):
        if(tile_exists(pos)):
            self.tileIDMap[pos["X"]][pos["Y"]] = 0

    #entferne tile aus allen spritegroups und füge in emptyTIle spritegroup
    def get_used_tiles(self):
        used = []
        for x in self.tileIDMap:
            for y in x:
                if(y != 0):
                    used.add(y)
        return used

    #muss noch lernen tile-Objekte zu verarbeiten
    def get_unused_tiles(self):
        unused = []
        for x in self.tileIDMap:
            for y in x:
                if(y == 0):
                    unused.add(y)
        return unused

    #gebe den aktuellen Build-Zustand zurück (bool)
    def is_build(self):
        return self.isBuild