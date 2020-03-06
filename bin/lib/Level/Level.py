import pygame, os, random
from bin.lib.Tile import Tile
from bin.config.generalCFG import NULL_TYPE, DEBUG, AVAILABLE_IMG_FORMAT_REGEX, SMOOTH_SCALE
from bin.config.levelCFG import *


#Lesen von Leveln muss noch implementiert werden
class Level:
    #konstruktor, ruft parse auf
    def __init__(self, levelFilePath = NULL_TYPE):
        self.parameters = { 
            "title": "Level",
            "levelFilePath": "",  # UNUSED #Datei-Pfad zu Ordner, der
            "difficulty": DEFAULT_LVL_CONF_PARAMETERS["difficulty"],
            "playerStartPositions": DEFAULT_LVL_CONF_PARAMETERS["playerStartPositions"]
        }
        self.gridSize = pygame.Rect(0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])  # zu kompatiblität ein rect. X und Y werden nicht mit einbezogen (vllt später als Position in der Arena?)
        self.currentTilePos = {"X": 0, "Y": 0}  # gibt an, welche tilePosition grade betrachtet wird (dient dem durchitereieren) 
        # diese 2D Liste wird zur Datenhaltung beim parsen und kompilieren des LevelFiles genutzt
        self.tileIDMap = []
        #tileGruppen:
        allTiles = pygame.sprite.LayeredUpdates
        animatedTiles = pygame.sprite.Group
        damagagingTiles = pygame.sprite.Group
        collidableTiles = pygame.sprite.Group

        # Zustands-Indikatoren für Level
        # Das level muss alle 3 Phasen nacheinander durchlaufen, um gefüllte SpriteGroups zu besitzen
        self.isParsed = False
        self.isCompiled = False
        self.isBuild = False

        # jede geladene tile aus dem TileSet wird hierein geparst und geladen
        self.parsedTileIDs = []
        DEBUG("Level.__init__(lvlDir = NULL_TYPE)", 0)
        DEBUG("Level.__init__:übergebener filePath",1 , levelFilePath)
        super().__init__()
        DEBUG("Level.__init__(lvlDir = NULL_TYPE): rufe Level.compile(filePath) auf", 1)
        if(os.path.isFile(levelFilePath) == False):
            #hier gäb es die Möglichkeit eine Suche ausgehend von übergebenem Pfad anstoßen und nach einem Ordner im übergelegenen Verzeichnis suchen
            DEBUG("Level.__init__(lvlDir = NULL_TYPE): Level-Directory nicht gefunden, überlasse das Problem den folgenden build-Prozess...", 0)
        self.compile(levelFilePath)
        DEBUG("Level.__init__(lvlDir = NULL_TYPE): Init abgeschlossen", 1)
    #gibt die GruppenID NachbarTiles der übergebenen Position zurück, wenn es ein äußeres Tile ist, dann nutze die RandTiles von der gegenüberliegende Seite mit, sodass ein endlosbildschirm entsteht
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
    #hier fehlt noch das abschneiden von dem string vor den Werten z.b. "grid="
    #Es fehlt noch das Einlesen des Dateinamens als levelTitel
    def parse_lvl_file(self, filePath = ""):
        self.isParsed = False
        self.isCompiled = False
        self.isBuild = False
        DEBUG("Level.parse_lvl_file(filePth)", 0)
        DEBUG("Level.parse_lvl_file: übergebener DateiPfad",1, filePath)
        self.parameters["playerStartPositions"] = DEFAULT_PLAYER_STARTPOS.copy()
            #optimierbar: erstellle für jede gefundene Datei ein unterlevel
        if(os.path.isFile(filePath)): #datei vorhanden?
                lvlFile = open(filePath, "r")
                self.parameters["title"] = lvlFile.name
                self.parameters["title"].replace("_"," ").replace(".lvl", "")
                DEBUG("Level.parse_lvl_file: Dateiname als LevelTitel ausgelesen",2, self.parameters["title"])
                DEBUG("Level.parse_lvl_file: Datei geöffnet:\n", 1) 
                DEBUG("Level.parse_lvl_file: DateiInhalt: ", 2, lvlFile)                  
                if(len(lvlFile) > 0): #inhalt nicht leer?
                    lvlData = lvlFile.replace(" ", "")
                    DEBUG("Level.parse_lvl_file: Datei getrimmt:\n", 2, lvlData)
                    rawLvl = DEFAULT_LVL_CONF_PARAMETERS.copy()
                    rawLvl["grid"].clear()
                    for line in lvlData:
                        DEBUG("Level.parse_lvl_file: parse Zeile:\n", 2, line)
                        for conditionName in DATA_CONDITIONS_LVL:
                            condition = DATA_CONDITIONS_LVL[conditionName]
                            DEBUG("Level.parse_lvl_file: nutze Zur Suche von" + conditionName + " diesen RegEx-Ausdruck: ", 3, condition)
                            results = re.search(condition, line)    #hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                            DEBUG("Level.parse_lvl_file: " + len(results) + "gefundene Zeile(n):\n", 5, results)
                            if(results[-1] != 'none'): 
                                if conditionName == "grid":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " grid Zeilen gefunden" , 4)
                                    for x in results:
                                        x = string.replace(x, "GRID=")
                                        tileTypeCols = x.split(';')

                                        DEBUG("Level.parse_lvl_file: " + len(tileTypeCols) + " grid Spalten in dieser zeile gefunden", 5 , x)

                                        if(len(tileTypeCols) > rawLvl["maxWidth"]):
                                            rawLvl["maxWidth"] = len(tileTypeCols)   
                                            DEBUG("Level.parse_lvl_file: längste Spalte gefunden, Tilemap hat jetzt " + rawLvl["maxWidth"] + " Spalten", 5)
                                        rawLvl["grid"].add(list(map(int, tileTypeCols))) #wandelt String-liste in int-liste um und fügt sie der tileIDMap zu
                                elif conditionName == "difficulty":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " difficulty Paramter gefunden, wähle: " , 4, results[-1])

                                    extractedDifficulties = list(map(int, results[-1].replace("difficulty=", ""))) #gruselige Zeile =)
                                    rawLvl["difficulty"] = extractedDifficulties[-1]
                                    
                                elif conditionName == "playerStartPos":
                                    DEBUG("Level.parse_lvl_file: " + len(results) + " playerStartPos Paramter gefunden, wähle: " , 4, results[-1])
                                    self.parameters["playerStartPositions"].clear()
                                    extractedplayerStartPositions = list(map(int, results[-1].replace("playerStartPos=", "")))
                                    startPosList = extractedplayerStartPositions[-1].split(')(')
                                    for x in startPosList:
                                        self.parameters["playerStartPositions"] = list(map(int, x.replace("(", "").replace(")", "").split(';') )) #gruselig =)
                                        DEBUG("Level.parse_lvl_file: füge (" + len(results) + " difficulty Paramter gefunden, wähle: " , 5, self.parameters["playerStartPositions"])
                            DEBUG("Level.parse_lvl_file: Zeile Abgeschlossen" , 3)
                            re.purge() #re-Chache leeren
                else: 
                    DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level", 1)
                    rawLvl = DEFAULT_LVL_CONF_PARAMETERS
                    self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird

        else:
            DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?", 1)
            rawLvl = DEFAULT_LVL_CONF_PARAMETERS
            
            self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])) #explizit festlegen, da normalerweise gridSize on the fly berechnet wird
        self.parameters["difficulty"] = rawLvl["difficulty"]
        self.parameters["title"] = rawLvl["title"]
        self.tileIDMap = rawLvl["grid"]
        self.gridSize = (0,0, (rawLvl["maxWidth"], len(self.tileIDMap)))
        DEBUG("Level.parse_lvl_file: nutze zum konfigurieren diese Werte: " , 0, rawLvl)
    #finde, lade und parse textureSetConf-File im übergebenen Verzeichnis in allTiles hinein
    def parse_texture_set(self):
        self.isParsed = False
        DEBUG("Level.parse_texture_set(levelPath)", 0)

        textureSetPath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
        DEBUG("Level.parse_texture_set(levelPath): öffne Textur Ordner an Pfad", 1, textureSetPath)
        if(os.path.isdir(textureSetPath) == False): #wenn texturOrdner nicht exisitiert -> DEFAULT-Textur-Ordner
            DEBUG("Level.parse_texture_set(levelPath): TexturPfad nicht gefunden. falle auf DefaultTexturSet zurück...", 1, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
            DEBUG("Level.parse_texture_set(levelPath): Falle auf DefaultTexturSet zurück...", 1, textureSetPath)
        foundConfFilePaths = glob.glob(os.path.join(textureSetPath, '') + '*.conf')
        if(foundConfFilePaths[-1] == "none" ): #wenn keine .conf-Datei gefunden -> DEFAULT-Textur-Ordner
            DEBUG("Level.parse_texture_set(levelPath): TexturPfad enthält keine Textur Datei/en(.conf).", 0, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
            DEBUG("Level.parse_texture_set(levelPath): Falle auf DefaultTexturSet zurück...", 1, textureSetPath)
        else:
            DEBUG("Level.parse_texture_set(levelPath): Liste gefundene Files auf", 3, foundConfFilePaths)
        #für jeden gefundenden .confFile ließ alle enthaltenen ParameterObjekte ein
        #finde alle conf dateien
        #gehe alle durch und appende die tileID liste (suche vor jedem Eintrag erst ob es deisen bereits gibt)
        #durchsuche .conf Datei mit regex nach Parametern wie bei parse_lvl_file
        #nutze dabei die in DATA_CONDITIONS_TILE enthaltenen RegEx Ausdrücke um jedes Objekt zu finden
        for confFilePath in foundConfFilePaths: 
            DEBUG("Level.parse_texture_set: Öffne DateiPfad ", 2, confFilePath)
            confFile = open(confFilePath, "r")
            DEBUG("Level.parse_texture_set: gelesener DateiInhalt:", 5, confFile)
            if(len(confFile) > 0): #inhalt nicht leer?
                confData = confFile.replace(" ", "")
                DEBUG("Level.parse_texture_set: Datei getrimmt zu", 2, confData)
                #hier die gesamte Datei in einen String laden
                confData = ""
                for line in confData:
                    DEBUG("Level.parse_texture_set: Erzeuge String mit zusammenhängenden DateiInhalt (für re.search()):\n", 2, line)
                    confData += line
                condition = TEXTURE_ID_BLOCK_REGEX
                DEBUG("Level.parse_texture_set: nutze zur Suche von ID-Blöcken folgenden RegEx-Ausdruck", 3, condition)
                results = re.search(condition, confData)
                DEBUG("Level.parse_texture_set: " + str(len(results)) + "gefundene ID-Blöcke:\n", 2)
                DEBUG("Level.parse_texture_set: ID Blöcke:", 5, results)
                re.purge()
                if(results[-1] != 'none'): #durchsuche jeden gefundenen ID Block
                    for x in results:
                        rawParameters = DEFAULT_TILE_CONF_PARAMETERS.copy()
                        DEBUG("Level.parse_texture_set: aktuell durchsuchter ID-Block", 5, x)
                        for conditionName in DATA_CONDITIONS_TILE:
                            DEBUG("Level.parse_texture_set: nutze zur Suche von " + str(conditionName) + "den Ausdruck " +str(condition), 3)
                            condition = DATA_CONDITIONS_TILE[conditionName]
                            results = re.search(condition, x)
                            #entferne alles was buchstaben und : bzw. = hat
                            if((results) > 0):
                                if(conditionName == "ID"):
                                        x.replace("ID:", "")
                                        x.replace("{", "")
                                        DEBUG("Level.parse_texture_set: ID-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["ID"] = temp[-1]
                                
                                elif(conditionName == "groupID"):
                                        x.replace("groupID=", "")
                                        DEBUG("Level.parse_texture_set: groupID-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["groupID"] = temp[-1]
                                
                                elif(conditionName == "isClippable"):
                                        x.replace("isClippable=", "")
                                        DEBUG("Level.parse_texture_set: isClippable-Wert ausgeschnitten", 4, x)
                                        temp = list(map(bool, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["isClippable"] = temp[-1]
                                
                                elif(conditionName == "isAnimated"):
                                        x.replace("isAnimated=", "")
                                        DEBUG("Level.parse_texture_set: isAnimated-Wert ausgeschnitten", 4, x)
                                        temp = list(map(bool, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["isAnimated"] = temp[-1]

                                elif(conditionName == "dmgNeededToDestroy"):
                                        x.replace("dmgNeededToDestroy=", "")
                                        DEBUG("Level.parse_texture_set: dmgNeededToDestroy-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["dmgNeededToDestroy"] = temp[-1]

                                elif(conditionName == "damageOnCollision"):
                                        x.replace("damageOnCollision=", "")
                                        DEBUG("Level.parse_texture_set: damageOnCollision-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["damageOnCollision"] = temp[-1]

                                elif(conditionName == "damageOverTime"):
                                        x.replace("damageOverTime=", "")
                                        DEBUG("Level.parse_texture_set: damageOverTime-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["damageOverTime"] = temp[-1]
                                elif(conditionName == "layerID"):
                                        x.replace("layerID=", "")
                                        DEBUG("Level.parse_texture_set: layerID-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["layerID"] = temp[-1]

                                elif(conditionName == "playMvSlowDown"):
                                        x.replace("playMvSlowDown=", "")
                                        DEBUG("Level.parse_texture_set: playMvSlowDown-Wert ausgeschnitten", 4, x)
                                        temp = list(map(int, x))
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, x)
                                        rawParameters["playMvSlowDown"] = temp[-1]
                                
                                elif(conditionName == "playerMvManipulation"):
                                        x.replace("playerMvManipulation=", "")
                                        DEBUG("Level.parse_texture_set: playerMvManipulation-Wert ausgeschnitten", 4, x)
                                        temp = x.split(",")
                                        if(len(temp) >= 2):
                                            temp[0].replace("[", "")
                                            temp[1].replace("]", "")
                                        else:
                                            DEBUG("Level.parse_texture_set: ausgelesene Liste hat zu wenig elemente, fallback auf default", 1, temp)
                                            temp = DEFAULT_TILE_CONF_PARAMETERS["playerMvManipulation"]
                                        DEBUG("Level.parse_texture_set: nach umwandlung", 5, temp)
                                        rawParameters["playerMvManipulation"] = list(map(int, temp[:2])) #wandle die ersten beiden elemente von temp in ints um
                                elif(conditionName == "preferredNeighborIDs"):
                                        x.replace("preferredNeighborIDs=", "")
                                        DEBUG("Level.parse_texture_set: preferredNeighborIDs-Wert ausgeschnitten", 4, x)
                                        firstSplit = x.split(",")
                                        neighbors = []
                                        for split in firstSplit:
                                            split.replace("[[", "")
                                            split.replace("]]", "")
                                            secondSplit = split.split("][")
                                            if(len(secondSplit) == 1):
                                                neighbors.append(secondSplit)
                                            elif(len(secondSplit) == 2):
                                                for x in secondSplit:
                                                    neighbors.append(x)
                                        DEBUG("Level.parse_texture_set: nach trimming und splitting", 5, neighbors)
                                        temp = list(map(int, neighbors))
                                        DEBUG("Level.parse_texture_set: nach umwandlung str->int", 5, temp)
                                        rawParameters["preferredNeighborIDs"] = neighbors
                                self.parsedTileIDs.append(rawParameters)
                            else:
                                rawParameters["ID"] = 0 #wenn ein Regex nicht gefunden wird, soll mit ID = 0 das eingelesene Paket ungültig gemacht werden
                            re.purge()
                    if(rawParameters["ID"] != 0): #wenn paket gültig
                        self.parsedTileIDs.append(rawParameters)   
                else:
                    DEBUG("Level.parse_texture_set: keine ID Blöcke gefunden, überspringe Block",1)    
            else: 
                DEBUG("Level.parse_texture_set: .conf Datei leer? versuche eine andere, wenn vorhanden", 1)

        self.isParsed = True
    #1. lade textureSetConf und beschreibe sämtliche geladenen Tiles mit den zu GroupID entsprechenden Eigenschaften
    #2. wähle im 2. Schritt die passende TileID(entsprechend der Neighbors) aus der geöffneten Gruppe aus
    #3. erstelle ein tile und übergebe den texturepfad des entsprechenden tiles
    #das bild wird erst mit build() geladen um zu verhindern dass alle lvl parallel offen sind
    def compile_lvl(self):
        if(self.isParsed):

            DEBUG("Level.compile()", 0)
            DEBUG("Level.compile(): rufe parse_lvl_file() auf", 1)
            self.parse_lvl_file()
            DEBUG("Level.compile(): rufe parse_texture_file() auf", 1)
            self.parse_texture_set()
            DEBUG("Level.compile(): abgeschlossen", 2)




            self.isCompiled = True
    #1. ließt alle tileIDs ein und lädt jewils die entsprechende textur
    #2. erstelle eine sprite.group mit sämtlichen tiles, passiven tiles, animierten tiles, 
    #wenn IS_BUILD_ON_UPDATE = True, dann wird mit jedem build aufruf nur ein tile erstellt und currentTilePos auf dieses gesetzt. 
    #(überprüfen lässt sich der aktuelle Build-Zustand mit bool self.isBuild())
    #gibt eine Liste mit übereinstimmungen 
    def match_neighbors(self, neighbors1 = [], neighbors2 = []):
        DEBUG("Level.match_neighbors(self, neighbors1 = [], neighbors2 = []):", 0)
        matches = []
        position = { "X": 0, "Y": 0}
        match = {"position": {}, "groupID": 0}
        if(len(neighbors1) == 3 & len(neighbors2) == 3):
            for list in neighbors1:
                if(len(list) == 3 & len(neighbors2[position["Y"]]) == 3):
                    for element in list:
                        DEBUG("Level.match_neighbors(): vergleiche Element an Position", 2, position)
                        if(element == neighbors2[position["X"]][position["Y"]]):
                            DEBUG("Level.match_neighbors(): match gefunden an", 3, position)
                            matches.append({"position": position, "groupID": element})
                        position["X"] += 1
                    position["Y"] += 1
                else:
                    DEBUG("Level.match_neighbors(): Listenlänge der neighborsListe[" + str(position["Y"]) +"] != 3", 0)
                    return None
            DEBUG("Level.match_neighbors(): gefundene Matches:", 2, matches)
            return matches
        else:
            DEBUG("Level.match_neighbors(): Listenlänge der neighbors stimmt nicht != 3", 0)
            return None
    #Berechne Größe eines einzelnen TIles und gebe ein entsprechendes Rect Objekt zurück (x und y = 0)
    def calc_tileSize(self):
        return pygame.Rect(0 , 0, ARENA_AREA.w // self.gridSize.x,ARENA_AREA.h // self.gridSize.y)
    #baut die Spieloberfläche mit sämtlichentiles auf
    def build(self):
        if(self.isCompiled):
            DEBUG("Level.build():", 0)
            if(IS_BUILD_ON_UPDATE):
                DEBUG("Level.build(): IS_BUILD_ON_UPDATE ist aktiv", 1, IS_BUILD_ON_UPDATE)
                if(self.tile_exists(self.currentTilePos)):
                    pass
            else:
                DEBUG("Level.build(): IS_BUILD_ON_UPDATE ist inaktiv", 1, IS_BUILD_ON_UPDATE)
                self.currentTilePos["X"] = 0
                self.currentTilePos["Y"] = 0
                DEBUG("Level.build(): betrachtete TileMap", 4, self.tileIDMap)
                for y in self.tileIDMap: 
                    for x in y:
                        #suche hier nach den nachbarn und der aktuellen position
                        self.currentTilePos["X"] = x
                        self.currentTilePos["Y"] = y
                        neighbors = self.get_neighbors(self.currentTilePos)
                        matchingTileIDConfs = []
                        for tileIDConf in self.parsedTileIDs:
                            if(tileIDConf["groupID"] == x):
                                matchingTileIDConfs.append(tileIDConf)
                        
                        tilesAndMatches = []
                        for tileIDConf in matchingTileIDConfs:
                            #rufe matchNeighbors auf und übergebe tileIDConf[neighbors] und self.getNeighbors(x)
                            matches = self.match_neighbors(tileIDConf["preferredNeighborIDs"], self.get_neighbors(self.currentTilePos))
                            if(matches != None):
                                #if(len(tileAndMatch["matches"]) < len(matches)):
                                
                                tilesAndMatches.append({"tileIDConf": tileIDConf, "matches" : matches})
                            else:
                                DEBUG("Level.build(): Fehler bei match_neighbors, überspringe dieses Tile", 0)

                            #sortiere Liste nach enthaltenen 'matchesAttributen'
                            DEBUG("Level.build(): gefundene Matches mit ihren Tiles:", 2, tilesAndMatches)
                            tilesAndMatches = sorted(tilesAndMatches, key=lambda k: k['matches'])
                            DEBUG("Level.build(): gefundene Matches mit ihren Tiles nach Sortierung:", 3, tilesAndMatches)
                            chosenID = tilesAndMatches[-1]


                        #Wir haben jetzt die exakte tileID n self.currentPosition {X,Y}
                        #-ermittle die größe eines einzelnen tiles OK
                        #-ermittle die Pixel-Position des ektuellen tiles mit 
                            #currentPos[X] * tileSize.w
                        tileRect = self.calc_tileSize()
                        tileRect.x = self.currentTilePos["X"] * tileRect.w
                        tileRect.x = self.currentTilePos["Y"] * tileRect.h
                        tileTexturePath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
                        newTile = Tile(tileRect ,tileTexturePath, chosenID["tileIDConf"])
                        if(newTile.has_animation()):
                            self.animatedTiles.add(newTile)
                        if(newTile.has_damage()):
                            self.damagingTiles.add(newTile)
                        if(newTile.has_collision()):
                            self.collidableTiles.add(newTile)
                        self.currentTilePos["X"] += 1 #wird benötigt um entsprechende Position des tiles zu bestimmen    
                    self.currentTilePos["Y"] += 1
            self.allTiles.add(self.animatedTiles, self.damagingTiles, self.collidableTiles)
            self.isBuid = True       
        else: DEBUG("Level.build() build wird nicht ausgeführt, level ist noch nicht compiliert...", 1)
        return self.allTiles
    #leert sämtliche Spritegruppen und zerstört dessen Tiles (Schafft platz im RAM)
    def unbuild(self):
        for sprite in self.allTiles:
            sprite.kill()
        self.isBuild = False
    #führe ein unload() aus und lade erneut mit load()
    def rebuild(self):
        self.unbuild()
        self.build()
    #gibt true zurück, wenn tile existiert
    def tile_exists(self, pos = {"X": 0, "Y": 0}):
        return (0 <= pos["Y"] < len(self.tileIDMap) & 0 <= pos["X"] < len(self.tileIDMap[pos["Y"]]))
    #gibt ID an entsprechender Position zurück (nach parsen, und vor build möglich (nach/während dem build zwar immernoch möglich, aber nichtmehr an die tiles gekoppelt))
    def get_tile_ID(self, pos = {"X": 0, "Y": 0}):
        if(self.tile_exists(pos)):
            return self.tileIDMap[pos["X"]][pos["Y"]]    
        else:
            return NULL_TYPE
    #gibt die tileID zurück
    def get_ID(self):
        return self.id
    #ändert tile in tileIDMap auf übergebenen groupID
    def set_tile(self, pos = {"X": 0, "Y": 0}, groupID = 0):
        if(self.tile_exists(pos)):
            self.tileIDMap[pos["X"]][pos["Y"]] = groupID
            return pos
        else:
            return NULL_TYPE
    #muss noch lernen tile-Objekte zu verarbeiten
    def unset_tile(self, pos ={"X": 0, "Y": 0}):
        if(self.tile_exists(pos)):
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

    def load_background(self):
        bg_dir = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "bg")
        results = glob.glob(bg_dir + "+." + AVAILABLE_IMG_FORMAT_REGEX)
        
        if(len(results) > 0):
            bg_path = results[random.randint(0, len(results) - 1)]
            if(os.path.isfile(bg_path)):
                bg_surface = pygame.Surface(ARENA_AREA.w, ARENA_AREA.h)
                bg_surface.fill((0,0,0), bg_surface.get_rect())
                bg = pygame.image.load(bg_path).convert()
                if(SMOOTH_SCALE):
                    pygame.transform.smoothscale(bg, (ARENA_AREA.w, ARENA_AREA.h))
                else:
                    pygame.transform.scale(bg, (ARENA_AREA.w, ARENA_AREA.h))
                
            