import pygame, os, random
from bin.lib.Tile import Tile
from bin.config.generalCFG import NULL_TYPE, DEBUG, AVAILABLE_IMG_FORMAT_REGEX, SMOOTH_SCALE
from bin.config.levelCFG import *


# Lesen von Leveln muss noch implementiert werden
class Level:
    # konstruktor, ruft parse auf
    def __init__(self, levelFilePath=""):
        super().__init__()
        DEBUG("Level.init(levelFilePath)", 1, levelFilePath)
        self.parameters = {
            "title": "Level",
            "levelFilePath": levelFilePath,  # hier kann später noch ein default-levelPath definiert werden
            "difficulty": DEFAULT_LVL_CONF_PARAMETERS["difficulty"],
            "playerStartPositions": DEFAULT_LVL_CONF_PARAMETERS["playerStartPositions"]
        }
        DEBUG("Standard Parameter voreingestellt", 2, self.parameters)
        self.gridSize = pygame.Rect(0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE[
            "Y"])  # Vorsicht!! statt pixelWerte wird hier die Anzahl an Tiles genutztzu kompatiblität ein rect. X und Y werden nicht mit einbezogen (vllt später als Position in der Arena?)
        DEBUG("Standard GridSize rect voreingestellt:", 3, self.gridSize)
        self.currentTilePos = {"X": 0,
                               "Y": 0}  # gibt an, welche tilePosition grade betrachtet wird (dient dem durchitereieren)
        # diese 2D Liste wird zur Datenhaltung beim parsen und kompilieren des LevelFiles genutzt
        self.tileIDMap = []
        # tileGruppen:
        self.allTiles = pygame.sprite.LayeredUpdates
        self.animatedTiles = pygame.sprite.Group
        self.damagingTiles = pygame.sprite.Group
        self.collidableTiles = pygame.sprite.Group

        # Zustands-Indikatoren für Level
        # Das level muss alle 3 Phasen nacheinander durchlaufen, um gefüllte SpriteGroups zu besitzen
        self.isParsed = False
        self.isCompiled = False
        self.isBuild = False

        # jede geladene tile aus dem TileSet wird hierein geparst und geladen
        self.parsedTileIDs = []

        DEBUG("rufe Level.compile(filePath) auf", 2)
        if (os.path.isfile(levelFilePath) == False):
            # hier gäb es die Möglichkeit eine Suche ausgehend von übergebenem Pfad anstoßen und nach einem Ordner im übergelegenen Verzeichnis suchen
            DEBUG(
                "Level-Directory nicht gefunden, überlasse das Problem den folgenden build-Prozess...",
                1)
        self.compile()
        DEBUG("Init abgeschlossen", 1)

    # gibt die GruppenID NachbarTiles der übergebenen Position zurück, wenn es ein äußeres Tile ist, dann nutze die RandTiles von der gegenüberliegende Seite mit, sodass ein endlosbildschirm entsteht

    def get_neighbors(self, position={"X": 0, "Y": 0}):
        DEBUG("Level.get_neighbors(position{})", 1, position)
        # ändere Position auf den oben linken nachbarn
        position["X"] -= 1
        position["Y"] -= 1
        currentNeighbor = position.copy()  # erstelle ein identisches dict zu position
        neighbors = []
        # gehe Alle 3 möglichen NachbarZeilen durch
        for y in range(3):
            # füge eine neue Y Liste hinzu
            neighbors.append(list())
            currentNeighbor["Y"] = position["Y"]
            currentNeighbor["Y"] += y
            DEBUG("Level.get_neighbors(position{}) wähle Y Position: " + str(currentNeighbor["Y"]), 3)
            # wenn Nachbar nicht vorhanden (Rand)
            # dann nehme entsrechenden randtile von der gegenüberliegenden Seite als nachbarn
            # erstellt eine von den tiles her eine endlos-Arena
            if (currentNeighbor["Y"] < 0):
                currentNeighbor["Y"] = (len(self.tileIDMap) - 1)
                DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + str(currentNeighbor["Y"]) + "als Nachbarn", 4)
            elif (currentNeighbor["Y"] >= (len(self.tileIDMap))):
                currentNeighbor["Y"] = 0
                DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + str(currentNeighbor["Y"]) + "als Nachbarn", 4)
            # wiederhole obiges für jedes Feld in aktueller Zeile
            for x in range(3):
                neighbors[-1].append(list())
                currentNeighbor["X"] = position["X"]  # currentNeighbor wird nach durchlauf manipuliert sein, setze current Neighbor zurück auf position(erste NachbarPos ecke oben links)
                currentNeighbor["X"] += x
                DEBUG("Level.get_neighbors(position{}) wähle X Position: " + str(currentNeighbor["X"]), 3)
                if (currentNeighbor["X"] < 0):
                    currentNeighbor["X"] = (len(self.tileIDMap[position["Y"]]) - 1)
                    DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle " + str(currentNeighbor["X"]) + " als Nachbarn",4)
                elif (currentNeighbor["X"] == (len(self.tileIDMap))):
                    currentNeighbor["X"] = 0
                    DEBUG("Level.get_neighbors(position{}) Rand erkannt, wähle" + str(currentNeighbor["X"]) + "als Nachbarn",
                          4)
                neighbors[y][x] = self.get_tile_ID(currentNeighbor)
        DEBUG("Level.get_neighbors(position{}) abgeschlossen", 2, neighbors)
        return neighbors

    # Lese .lvl Datei (debugging implementiert)
    # hier fehlt noch das abschneiden von dem string vor den Werten z.b. "grid="
    # Es fehlt noch das Einlesen des Dateinamens als levelTitel

    def parse_lvl_file(self, filePath = ""):
        self.isParsed = False
        self.isCompiled = False
        self.isBuild = False
        if(filePath == ""):
            filePath = self.parameters["levelFilePath"]
        DEBUG("Level.parse_lvl_file(filePth)", 0)
        DEBUG("übergebener DateiPfad", 1, filePath)
        self.parameters["playerStartPositions"] = DEFAULT_PLAYER_STARTPOS.copy()
        # optimierbar: erstellle für jede gefundene Datei ein unterlevel
        if (os.path.isfile(filePath)):  # datei vorhanden?
            lvlFileObj = open(filePath, "r")
            self.parameters["title"] = lvlFileObj.name
            self.parameters["title"].replace("_", " ").replace(".lvl", "")
            DEBUG("Dateiname als LevelTitel ausgelesen", 2, self.parameters["title"])
            DEBUG("Datei geöffnet:\n", 1)
            DEBUG("DateiInhalt: ", 2, lvlFileObj)
            lvlFile = []
            for line in lvlFileObj:
                lvlFile.append(line)
            lvlFileObj.close()
            DEBUG("Datei in Stringliste umgewandelt:", 3, lvlFile)
            if (len(lvlFile) > 0):  # inhalt nicht leer?
                lvlData = []
                for x in lvlFile:
                    x = x.replace(" ", "")
                    lvlData.append(x)
                DEBUG("Datei getrimmt und Platzhalter gefüllt:", 3, lvlData)
                rawLvl = DEFAULT_LVL_CONF_PARAMETERS.copy()
                rawLvl["grid"].clear()
                for line in lvlData:
                    DEBUG("", 2)
                    DEBUG("Parse nächste Zeile:", 2, line.replace("\n", ""))
                    #DEBUG("nutze konditionen in angegebener Reihenfolge", 4, DATA_CONDITIONS_LVL)
                    for conditionName in DATA_CONDITIONS_LVL:
                        condition = DATA_CONDITIONS_LVL[conditionName]
                        DEBUG("nutze Zur Suche von " + conditionName + " diesen RegEx-Ausdruck: ", 4, condition)
                        results = re.findall(condition, line)  # hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                        if (len(results) > 0):
                            DEBUG("gefundene Zeile(n):", 5, results)
                            if conditionName == "grid":
                                temp = []
                                tileGroupID_X = []
                                for x in results:
                                    DEBUG("vor replace " + str(x), 6)
                                    x = x.replace("GRID=", "")
                                    DEBUG("nach replace " + str(x), 6)
                                    temp = x.split(';')
                                    DEBUG("gesplittet",9, temp)
                                    for value in temp:
                                        DEBUG("speichere " + str(value), 8)
                                        tileGroupID_X.append(int(value))
                                        DEBUG("Füge diese Zeile dem Grid hinzu", 11, tileGroupID_X)
                                    if (len(tileGroupID_X) > rawLvl["maxWidth"]):
                                        rawLvl["maxWidth"] = len(tileGroupID_X)
                                        DEBUG("bisher längste Spalte gefunden, Tilemap hat jetzt " + str(rawLvl["maxWidth"]) + " Spalten", 7)
                                    rawLvl["grid"].append(tileGroupID_X)
                                    DEBUG(str(len(tileGroupID_X)) + " grid Spalten gefunden", 7)
                                DEBUG("grid hat jetzt " + str(len(rawLvl["grid"])) + " Zeilen", 7)
                            elif conditionName == "difficulty":
                                DEBUG("difficulty Paramter gefunden, wähle: ", 4, results[-1])

                                extractedDifficulty = int(results[-1].replace("difficulty=", ""))  # gruselige Zeile =)
                                rawLvl["difficulty"] = extractedDifficulty
                                DEBUG("extrahierter difficulty wert: ", 4, extractedDifficulty)

                            elif conditionName == "playerStartPos":
                                DEBUG("playerStartPos Paramter gefunden, wähle: ", 4, results[-1])
                                self.parameters["playerStartPositions"].clear()
                                extractedplayerStartPositions = results[-1].replace("playerStartPos=", "")
                                DEBUG("extrahierte StartPositionen ", 5, extractedplayerStartPositions)
                                startPosList = extractedplayerStartPositions.split(')(')
                                DEBUG("ausgelesene Startpositions-Pärchen:", 6, startPosList)
                                for x in startPosList:
                                    x = x.replace("(", "")
                                    x = x.replace(")", "")
                                    x = x.split(";")
                                    temp = []
                                    if(len(x) == 2):
                                        for value in x:
                                            temp.append(int(value))
                                        self.parameters["playerStartPositions"].append(temp)
                                    DEBUG("ermittelte StartPositionen", 4 ,self.parameters["playerStartPositions"])
                        DEBUG("wechsle auf nächsten Regex-Ausdruck", 4)
                        re.purge()  # re-Chache leeren
                        results.clear()
            else:
                DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level", 1)
                rawLvl = DEFAULT_LVL_CONF_PARAMETERS
                self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"]))  # explizit festlegen, da normalerweise gridSize on the fly berechnet wird

        else:
            DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?", 1)
            rawLvl = DEFAULT_LVL_CONF_PARAMETERS

            self.gridSize = (0, 0, (DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE[
                "Y"]))  # explizit festlegen, da normalerweise gridSize on the fly berechnet wird
        self.parameters["difficulty"] = rawLvl["difficulty"]
        self.parameters["title"] = rawLvl["title"]
        self.tileIDMap = rawLvl["grid"]
        self.gridSize = (0, 0, (rawLvl["maxWidth"], len(self.tileIDMap)))
        DEBUG("nutze zum konfigurieren diese Werte: ", 11, rawLvl)
        DEBUG("---Level erstellt---", 0)
        DEBUG(".lvl-Parsing abgeschlossen", 1)
    # finde, lade und parse textureSetConf-File im übergebenen Verzeichnis in allTiles hinein

    def parse_texture_set(self):
        self.isParsed = False
        DEBUG("Level.parse_texture_set(levelPath)", 0)

        textureSetPath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
        DEBUG("öffne Textur Ordner an Pfad", 1, textureSetPath)
        if (os.path.isdir(textureSetPath) == False):  # wenn texturOrdner nicht exisitiert -> DEFAULT-Textur-Ordner
            DEBUG("TexturPfad nicht gefunden. falle auf DefaultTexturSet zurück...",
                  1, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
            DEBUG("Falle auf DefaultTexturSet zurück...", 1, textureSetPath)
        textureSetConfRegex = os.path.join(textureSetPath, '') + '*.conf'
        DEBUG("suche nach confFiles mit diesem Ausdruck", 2, textureSetConfRegex)
        foundConfFilePaths = glob.glob(textureSetConfRegex)
        DEBUG("diese Files wurden gefunden", 10, foundConfFilePaths)
        if(len(foundConfFilePaths) > 0):
            if (foundConfFilePaths[-1] == "none"):  # wenn keine .conf-Datei gefunden -> DEFAULT-Textur-Ordner
                DEBUG("TexturPfad enthält keine Textur Datei/en(.conf).", 0,
                      textureSetPath)
                textureSetPath = DEFAULT_TEXTURE_SET_PATH
                DEBUG("Falle auf DefaultTexturSet zurück...", 1, textureSetPath)
            else:
                DEBUG("Liste gefundene Files auf", 3, foundConfFilePaths)
            # für jeden gefundenden .confFile ließ alle enthaltenen ParameterObjekte ein
            # finde alle conf dateien
            # gehe alle durch und appende die tileID liste (suche vor jedem Eintrag erst ob es deisen bereits gibt)
            # durchsuche .conf Datei mit regex nach Parametern wie bei parse_lvl_file
            # nutze dabei die in DATA_CONDITIONS_TILE enthaltenen RegEx Ausdrücke um jedes Objekt zu finden
            for confFilePath in foundConfFilePaths:
                DEBUG("Öffne DateiPfad ", 2, confFilePath)
                confFile = open(confFilePath, "r")
                confData = ""
                DEBUG("gelesener DateiInhalt:", 10, confFile)
                for x in confFile:
                    confData += str(x)
                confFile.close()
                confData = confData.replace("\n", "")
                confData = confData.replace(" ", "")
                if (len(confData) > 0):  # inhalt nicht leer?
                    DEBUG("Datei getrimmt zu", 6, confData)
                    condition = TEXTURE_ID_BLOCK_REGEX
                    DEBUG("nutze zur Suche von ID-Blöcken folgenden RegEx-Ausdruck", 3, condition)
                    results = re.findall(condition, confData)
                    DEBUG(str(len(results)) + " gefundene ID-Blöcke:", 2)
                    DEBUG("gefundene ID Blöcke:", 6, results)
                    re.purge()
                    if (len(results) > 0):  # durchsuche jeden gefundenen ID Block
                        for idBlock in results:
                            rawParameters = DEFAULT_TILE_CONF_PARAMETERS.copy()
                            DEBUG("aktuell durchsuchter ID-Block", 7, idBlock)
                            for conditionName in DATA_CONDITIONS_TILE:
                                condition = DATA_CONDITIONS_TILE[conditionName]
                                DEBUG("nutze zur Suche von " + str(conditionName) + " den Ausdruck " + str(condition), 5)
                                resultsInBlock = re.findall(condition, idBlock)
                                DEBUG(str(len(resultsInBlock)) + " gefundene Elemente", 6, resultsInBlock)
                                if (len(resultsInBlock) > 0):
                                    if (conditionName == "ID"):
                                        x = resultsInBlock[-1]
                                        x = x.replace("ID:", "")
                                        x = x.replace("{", "")
                                        DEBUG("ID-Wert ausgeschnitten", 6, x)
                                        
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["ID"] = int(x)

                                    elif (conditionName == "groupID"):
                                        x = resultsInBlock[-1].replace("groupID=", "")
                                        DEBUG("groupID-Wert ausgeschnitten", 6, x)
                                        
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["groupID"] = int(x)

                                    elif (conditionName == "isClippable"):
                                        x = resultsInBlock[-1].replace("isClippable=", "")
                                        DEBUG("isClippable-Wert ausgeschnitten", 4, x)
                                        DEBUG("nach umwandlung", 5, bool(int(x)))
                                        rawParameters["isClippable"] = bool(int(x))

                                    elif (conditionName == "isAnimated"):
                                        x = resultsInBlock[-1].replace("isAnimated=", "")
                                        DEBUG("isAnimated-Wert ausgeschnitten", 4, x)
                                        DEBUG("nach umwandlung", 5, bool(int(x)))
                                        rawParameters["isAnimated"] = bool(int(x))

                                    elif (conditionName == "dmgNeededToDestroy"):
                                        x = resultsInBlock[-1].replace("dmgNeededToDestroy=", "")
                                        DEBUG("dmgNeededToDestroy-Wert ausgeschnitten", 4, x)
                                        DEBUG("nach umwandlung", 5, int(x))
                                        rawParameters["dmgNeededToDestroy"] = int(x)

                                    elif (conditionName == "damageOnCollision"):
                                        x = resultsInBlock[-1].replace("damageOnCollision=", "")
                                        DEBUG("damageOnCollision-Wert ausgeschnitten", 4, x)
                                        
                                        DEBUG("nach umwandlung", 5, int(x))
                                        rawParameters["damageOnCollision"] = int(x)

                                    elif (conditionName == "damageOverTime"):
                                        x = resultsInBlock[-1].replace("damageOverTime=", "")
                                        DEBUG("damageOverTime-Wert ausgeschnitten", 4, x)
                                        
                                        DEBUG("nach umwandlung", 5, int(x))
                                        rawParameters["damageOverTime"] = int(x)
                                    elif (conditionName == "layerID"):
                                        x = resultsInBlock[-1].replace("layerID=", "")
                                        DEBUG("layerID-Wert ausgeschnitten", 4, x)
                                        rawParameters["layerID"] = int(x)
                                        DEBUG("nach umwandlung", 5, int(x))
                                        rawParameters["layerID"] = int(x)

                                    elif (conditionName == "playMvSlowDown"):
                                        x = resultsInBlock[-1].replace("playMvSlowDown=", "")
                                        DEBUG("playMvSlowDown-Wert ausgeschnitten", 4, x)
                                        
                                        DEBUG("nach umwandlung", 5, int(x))
                                        rawParameters["playMvSlowDown"] = int(x)

                                    elif (conditionName == "playerMvManipulation"):
                                        x = resultsInBlock[-1].replace("playerMvManipulation=", "")
                                        DEBUG("playerMvManipulation-Wert ausgeschnitten", 4, x)
                                        temp = x.split(",")
                                        if (len(temp) == 2):
                                            temp[0] = int(temp[0].replace("[", ""))
                                            temp[1] = int(temp[1].replace("]", ""))
                                        else:
                                            DEBUG("ausgelesene Liste hat zu wenig/viele elemente, fallback auf default",1, temp)
                                            temp = DEFAULT_TILE_CONF_PARAMETERS["playerMvManipulation"]
                                        DEBUG("nach umwandlung", 5, temp)
                                        rawParameters["playerMvManipulation"].append(int(temp[0])) 
                                        rawParameters["playerMvManipulation"].append(int(temp[0])) # wandle die ersten beiden elemente von temp in ints um
                                    elif (conditionName == "preferredNeighborIDs"):
                                        x = resultsInBlock[-1].replace("preferredNeighborIDs=", "")
                                        DEBUG("preferredNeighborIDs-Wert ausgeschnitten", 4, x)
                                        firstSplit = x.split(",")
                                        neighbors = []
                                        for split in firstSplit:
                                            split.replace("[[", "")
                                            split.replace("]]", "")
                                            secondSplit = split.split("][")
                                            if (len(secondSplit) == 1):
                                                neighbors.append(secondSplit)
                                            elif (len(secondSplit) == 2):
                                                for x in secondSplit:
                                                    neighbors.append(int(x))
                                        DEBUG("nach trimming und splitting", 5, neighbors)
                                        DEBUG("nach umwandlung str->int", 5, temp)
                                        rawParameters["preferredNeighborIDs"] = neighbors
                                    self.parsedTileIDs.append(rawParameters)
                                else:
                                    rawParameters["ID"] = 0  # wenn ein Regex nicht gefunden wird, soll mit ID = 0 das eingelesene Paket ungültig gemacht werden
                                re.purge()
                        if (rawParameters["ID"] != 0):  # wenn paket gültig
                            self.parsedTileIDs.append(rawParameters)
                    else:
                        DEBUG("keine ID Blöcke gefunden, überspringe Datei", 2)
                else:
                    DEBUG(".conf Datei leer?, überspringe diese Datei", 2)

            self.isParsed = True
        else:
            DEBUG("es wurden keine textur-Configs gefunden!!, alle geladenen Blöcke die != 0 sind werden einfarbig")

    # 1. lade textureSetConf und beschreibe sämtliche geladenen Tiles mit den zu GroupID entsprechenden Eigenschaften
    # 2. wähle im 2. Schritt die passende TileID(entsprechend der Neighbors) aus der geöffneten Gruppe aus
    # 3. erstelle ein tile und übergebe den texturepfad des entsprechenden tiles
    # das bild wird erst mit build() geladen um zu verhindern dass alle lvl parallel offen sind

    def compile(self):
        if (not self.isParsed):

            DEBUG("Level.compile()", 1)
            DEBUG("rufe parse_lvl_file() auf", 2)
            self.parse_lvl_file()
            DEBUG("rufe parse_texture_file() auf", 2)
            self.parse_texture_set()
            DEBUG("Kompilierung abgeschlossen", 1)
        else:
            DEBUG("Level ist bereits geparst und kompiliert", 1)
        self.isCompiled = True

    # 1. ließt alle tileIDs ein und lädt jewils die entsprechende textur
    # 2. erstelle eine sprite.group mit sämtlichen tiles, passiven tiles, animierten tiles,
    # wenn IS_BUILD_ON_UPDATE = True, dann wird mit jedem build aufruf nur ein tile erstellt und currentTilePos auf dieses gesetzt.
    # (überprüfen lässt sich der aktuelle Build-Zustand mit bool self.isBuild())
    # gibt eine Liste mit übereinstimmungen
    def match_neighbors(self, neighbors1=[], neighbors2=[]):
        DEBUG("Level.match_neighbors(self, neighbors1 = [], neighbors2 = []):", 0)
        matches = []
        position = {"X": 0, "Y": 0}
        match = {"position": {}, "groupID": 0}
        if (len(neighbors1) == 3 & len(neighbors2) == 3):
            for list in neighbors1:
                if (len(list) == 3 & len(neighbors2[position["Y"]]) == 3):
                    for element in list:
                        DEBUG("Level.match_neighbors(): vergleiche Element an Position", 2, position)
                        if (element == neighbors2[position["X"]][position["Y"]]):
                            DEBUG("Level.match_neighbors(): match gefunden an", 3, position)
                            matches.append({"position": position, "groupID": element})
                        position["X"] += 1
                    position["Y"] += 1
                else:
                    DEBUG("Level.match_neighbors(): Listenlänge der neighborsListe[" + str(position["Y"]) + "] != 3", 0)
                    return None
            DEBUG("Level.match_neighbors(): gefundene Matches:", 2, matches)
            return matches
        else:
            DEBUG("Level.match_neighbors(): Listenlänge der neighbors stimmt nicht != 3", 0)
            return None

    # Berechne Größe eines einzelnen TIles und gebe ein entsprechendes Rect Objekt zurück (x und y = 0)
    def calc_tileSize(self):
        return pygame.Rect(0, 0, ARENA_AREA.w // self.gridSize.x, ARENA_AREA.h // self.gridSize.y)

    # baut die Spieloberfläche mit sämtlichentiles auf
    def build(self):
        if (self.isCompiled):
            DEBUG("Level.build():", 0)
            if (IS_BUILD_ON_UPDATE):
                DEBUG("Level.build(): IS_BUILD_ON_UPDATE ist aktiv", 1, IS_BUILD_ON_UPDATE)
                if (self.tile_exists(self.currentTilePos)):
                    pass
            else:
                DEBUG("Level.build(): IS_BUILD_ON_UPDATE ist inaktiv", 1, IS_BUILD_ON_UPDATE)
                self.currentTilePos["X"] = 0
                self.currentTilePos["Y"] = 0
                DEBUG("Level.build(): betrachtete TileMap", 4, self.tileIDMap)
                temp = 0
                for y in self.tileIDMap:
                    for x in y:
                        # suche hier nach den nachbarn und der aktuellen position
                        neighbors = self.get_neighbors(self.currentTilePos)
                        matchingTileIDConfs = []
                        for tileIDConf in self.parsedTileIDs:
                            if (tileIDConf["groupID"] == x):
                                matchingTileIDConfs.append(tileIDConf)

                        tilesAndMatches = []
                        for tileIDConf in matchingTileIDConfs:
                            # rufe matchNeighbors auf und übergebe tileIDConf[neighbors] und self.getNeighbors(x)
                            matches = self.match_neighbors(tileIDConf["preferredNeighborIDs"],
                                                           self.get_neighbors(self.currentTilePos))
                            if (matches != None):
                                # if(len(tileAndMatch["matches"]) < len(matches)):

                                tilesAndMatches.append({"tileIDConf": tileIDConf, "matches": matches})
                            else:
                                DEBUG("Level.build(): Fehler bei match_neighbors, überspringe dieses Tile", 0)

                            # sortiere Liste nach enthaltenen 'matchesAttributen'
                            DEBUG("Level.build(): gefundene Matches mit ihren Tiles:", 2, tilesAndMatches)
                            tilesAndMatches = sorted(tilesAndMatches, key=lambda k: k['matches'])
                            DEBUG("Level.build(): gefundene Matches mit ihren Tiles nach Sortierung:", 3,
                                  tilesAndMatches)
                            if(len(tilesAndMatches) > 0):
                                chosenID = tilesAndMatches[-1]
                                DEBUG("bestes match =", 3, chosenID)
                            else:
                                chosenID = 1
                                DEBUG("matchesListe ist leer, versuche ID = 1 als bestes Match", 3, tilesAndMatches)
                        # Wir haben jetzt die exakte tileID n self.currentPosition {X,Y}
                        # -ermittle die größe eines einzelnen tiles OK
                        # -ermittle die Pixel-Position des ektuellen tiles mit
                        # currentPos[X] * tileSize.w
                        tileRect = self.calc_tileSize()
                        tileRect.x = self.currentTilePos["X"] * tileRect.w
                        tileRect.x = self.currentTilePos["Y"] * tileRect.h
                        tileTexturePath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture",
                                                       "tiles")
                        newTile = Tile(tileRect, tileTexturePath, chosenID["tileIDConf"])
                        if (newTile.has_animation()):
                            self.animatedTiles.add(newTile)
                        if (newTile.has_damage()):
                            self.damagingTiles.add(newTile)
                        if (newTile.has_collision()):
                            self.collidableTiles.add(newTile)
                        self.currentTilePos["X"] += 1  # wird benötigt um entsprechende Position des tiles zu bestimmen
                    self.currentTilePos["Y"] += 1
            self.allTiles.add(self.animatedTiles)
            self.allTiles.add(self.damagingTiles)
            self.allTiles.add(self.collidableTiles)
            
            self.isBuid = True
        else:
            DEBUG("Level.build() build wird nicht ausgeführt, level ist noch nicht compiliert...", 1)
        return self.allTiles

    # leert sämtliche Spritegruppen und zerstört dessen Tiles (Schafft platz im RAM)
    def unbuild(self):
        for sprite in self.allTiles:
            sprite.kill()
        self.isBuild = False

    # führe ein unload() aus und lade erneut mit load()
    def rebuild(self):
        self.unbuild()
        self.build()

    # gibt true zurück, wenn tile existiert
    def tile_exists(self, pos={"X": 0, "Y": 0}):
        return (0 <= pos["Y"] < len(self.tileIDMap) & 0 <= pos["X"] < len(self.tileIDMap[pos["Y"]]))

    # gibt ID an entsprechender Position zurück (nach parsen, und vor build möglich (nach/während dem build zwar immernoch möglich, aber nichtmehr an die tiles gekoppelt))
    def get_tile_ID(self, pos={"X": 0, "Y": 0}):
        if (self.tile_exists(pos)):
            return self.tileIDMap[pos["X"]][pos["Y"]]
        else:
            return NULL_TYPE

    # gibt die tileID zurück
    def get_ID(self):
        return self.id

    # ändert tile in tileIDMap auf übergebenen groupID
    def set_tile(self, pos={"X": 0, "Y": 0}, groupID=0):
        if (self.tile_exists(pos)):
            self.tileIDMap[pos["X"]][pos["Y"]] = groupID
            return pos
        else:
            return NULL_TYPE

    # muss noch lernen tile-Objekte zu verarbeiten
    def unset_tile(self, pos={"X": 0, "Y": 0}):
        if (self.tile_exists(pos)):
            self.tileIDMap[pos["X"]][pos["Y"]] = 0

    # entferne tile aus allen spritegroups und füge in emptyTIle spritegroup
    def get_used_tiles(self):
        used = []
        for x in self.tileIDMap:
            for y in x:
                if (y != 0):
                    used.add(y)
        return used

    # muss noch lernen tile-Objekte zu verarbeiten
    def get_unused_tiles(self):
        unused = []
        for x in self.tileIDMap:
            for y in x:
                if (y == 0):
                    unused.add(y)
        return unused

    # gebe den aktuellen Build-Zustand zurück (bool)
    def is_build(self):
        return self.isBuild
