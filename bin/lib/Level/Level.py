import pygame, os, random
from bin.lib.Tile import Tile
from bin.config.generalCFG import NULL_TYPE, AVAILABLE_IMG_FORMAT_REGEX, SMOOTH_SCALE, DEBUG
from bin.config.levelCFG import *
#from bin.lib.tools.tools import debug_logger as DEBUG

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
        self.gridSize = pygame.Rect(0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])  # Vorsicht!! statt pixelWerte wird hier die Anzahl an Tiles genutztzu kompatiblität ein rect. X und Y werden nicht mit einbezogen (vllt später als Position in der Arena?)
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

        
        if (os.path.isfile(levelFilePath) == False):
            # hier gäb es die Möglichkeit eine Suche ausgehend von übergebenem Pfad anstoßen und nach einem Ordner im übergelegenen Verzeichnis suchen
            DEBUG("Der übergebene Pfad enthält keine Datei. Versuche mit Default-Parametern fortzusetzen...",1)
        DEBUG("rufe Level.parse() auf", 2)
        self.parse()
        DEBUG("Init abgeschlossen", 1)

    def iter_currentPos(self):
        if(self.currentTilePos["X"] < len(self.tileIDMap[self.currentTilePos["Y"]])):
            self.currentTilePos["X"] += 1
        else:
            self.currentTilePos["X"] = 0
            if(self.currentTilePos["Y"] < len(self.tileIDMap)):
                self.currentTilePos["Y"] += 1
            else:
                self.currentTilePos["Y"] = 0

# gibt die GruppenID NachbarTiles der übergebenen Position zurück, wenn es ein äußeres Tile ist, dann nutze die RandTiles von der gegenüberliegende Seite mit, sodass ein endlosbildschirm entsteht
    def get_neighbors(self, position={"X": 0, "Y": 0}):
        if(position=={"X": 0, "Y": 0}):
            position = self.currentTilePos
        DEBUG("Level.get_neighbors(position{})", 4, position)
        # ändere Position auf den oben linken nachbarn
        neighbors = []
        # gehe Alle 3 möglichen NachbarZeilen durch
        for y in range(-1, 2):
            # füge eine neue Y Liste hinzu
            neighbors.append(list())
            line = position["Y"] + y
            DEBUG("wähle Zeile: " + str(line), 5)
            # wenn Nachbar nicht vorhanden (Rand)
            # dann nehme entsrechenden randtile von der gegenüberliegenden Seite als nachbarn
            # erstellt eine von den tiles her eine endlos-Arena
            if (line < 0):
                line = (len(self.tileIDMap) - 1)
                DEBUG("oberen Rand erkannt, wähle gegenüberliegende Seite (Zeile " + str(line) + ") als benachbarte Zeile", 6)
            elif (line >= (len(self.tileIDMap))):
                line = 0
                DEBUG("unteren Rand erkannt, wähle gegenüberliegende Seite (Zeile " + str(line) + ") als benachbarte Zeile", 6)
            # wiederhole obiges für jedes Feld in aktueller Zeile
            for x in range(-1, 2):
                pos = position["X"] + x 
                DEBUG("wähle Position " + str(pos), 6)
                if (pos < 0):
                    pos = (len(self.tileIDMap[line]) - 1)
                    DEBUG("linken Rand erkannt, wähle gegenüberliegende Seite (Spalte " + str(pos) + ") als benachbarte Spalte", 7)
                elif (pos >= (len(self.tileIDMap[line]))):
                    pos = 0
                    DEBUG("rechten Rand erkannt, wähle gegenüberliegende Seite (Spalte " + str(pos) + ") als benachbarte Spalte", 7)
                neighbors[-1].append(self.tileIDMap[line][pos])
        DEBUG("übergebe generierte NachbarListe zurück", 4, neighbors)
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
            DEBUG("Datei in Stringliste umgewandelt:", 4, lvlFile)
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
                    DEBUG("Parse Zeile:", 2, line.replace("\n", ""))
                    #DEBUG("nutze konditionen in angegebener Reihenfolge", 4, DATA_CONDITIONS_LVL)
                    for conditionName in DATA_CONDITIONS_LVL:
                        condition = DATA_CONDITIONS_LVL[conditionName]
                        DEBUG("Nutze zur Suche von " + conditionName + " den Ausdruck " + str(condition), 3)
                        results = re.findall(condition, line)  # hier testen, ob auch lvlFile übergeben werden kann (denn dann ist zeile 32 unnötig)
                        if (len(results) > 0):
                            DEBUG("gefundene Zeile(n):", 4, results)
                            if conditionName == "grid":
                                newGridLine = []
                                for x in results:
                                    DEBUG("ausgelesene Grid-Zeile: " + str(x), 6)
                                    x = x.replace("GRID=", "")
                                    DEBUG("nach replace " + str(x), 7)
                                    x = x.split(';')
                                    DEBUG("gesplittet (beinhaltet noch String Werte)" + str(x) ,7)
                                    for value in x:
                                        DEBUG("speichere " + str(value) + " als Integer", 8)
                                        newGridLine.append(int(value))
                                    DEBUG(str(len(newGridLine)) + " Elemente in Grid-Zeile", 6)
                                    DEBUG("Inhalt der neuen Zeile nach der Umwandlung:", 6, newGridLine)
                                    if(len(rawLvl["grid"]) > 0):
                                        if (len(newGridLine) > len(rawLvl["grid"][0])):
                                            DEBUG("bisher längste Zeile gefunden, Tilemap wird auf " + str(len(newGridLine)) + " Spalten erweitert", 8)
                                            for tileLineID in range(len(rawLvl["grid"])):
                                                tilesToAdd = len(newGridLine) - rawLvl["grid"]
                                                DEBUG("erweitere Zeile" + str(tileLineID) + "/" + str(len(rawLvl["grid"]) - 2), 9)
                                                DEBUG("alte Zeilen-Länge:" + str(len(self.rawLvl["grid"][tileLineID])), 10)
                                                DEBUG("gebe Inhalt von Zeile " + str(tileLineID) + "(unbearbeitet) aus:", 11, rawLvl["grid"][tileLineID])
                                                if(tilesToAdd > 0):
                                                    DEBUG("füge " + str(tilesToAdd) + "Spalten hinzu", 10)
                                                    for col in range(tilesToAdd):
                                                        DEBUG("erweitere Grid-Zeile " + str(tileLineID) + " um " + str(DEFAULT_UNKNOWN_TILE_ID), 12)
                                                        rawLvl["grid"][tileLineID].append(DEFAULT_UNKNOWN_TILE_ID)
                                                    DEBUG("gebe Zeile " + str(tileLineID) + "(bearbeitet) aus:", 11, rawLvl["grid"][tileLineID])
                                                    DEBUG("neue Zeilen-Länge " + str(len(rawLvl["grid"][tileLineID])), 10)
                                                else:
                                                    DEBUG("tilesToAdd ist <= 0", 10 ,tilesToAdd)
                                        else:
                                            DEBUG("Zeile ist gleichlang", 9)
                                            #hier könnte noch ein fehler sein!!! wenn eine Zeile kürzer als andere ist wird diese glaub ich nicht aufgefüllt
                                    rawLvl["grid"].append(newGridLine)
                                DEBUG("Grid-Zeile eingefügt. Grid hat jetzt " + str(len(rawLvl["grid"])) + " Zeilen", 3)
                            elif conditionName == "difficulty":
                                DEBUG("difficulty Paramter gefunden, wähle: ", 6, results[-1])

                                extractedDifficulty = int(results[-1].replace("difficulty=", ""))  # gruselige Zeile =)
                                rawLvl["difficulty"] = extractedDifficulty
                                DEBUG("Difficulty-Wert " + str(rawLvl["difficulty"]) + " eingelesen", 3)

                            elif conditionName == "playerStartPos":
                                DEBUG("playerStartPos Paramter gefunden, wähle: ", 6, results[-1])
                                rawLvl["playerStartPositions"].clear()
                                extractedplayerStartPositions = results[-1].replace("playerStartPos=", "")
                                DEBUG("extrahierte StartPositionen ", 7, extractedplayerStartPositions)
                                startPosList = extractedplayerStartPositions.split(')(')
                                DEBUG("ausgelesene Startpositions-Pärchen:", 7, startPosList)
                                for x in startPosList:
                                    x = x.replace("(", "")
                                    x = x.replace(")", "")
                                    x = x.split(";")
                                    temp = []
                                    if(len(x) == 2):
                                        for value in x:
                                            temp.append(int(value))
                                        rawLvl["playerStartPositions"].append(temp)
                                    DEBUG("Player-Startpositionen " + str(rawLvl["difficulty"]) + " eingelesen", 3)
                        DEBUG("Ausdruck abgeschlossen", 3)
                        re.purge()  # re-Chache leeren
                        results.clear()
            else:
                DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (leer?) falle zurück auf Default Level", 1)
                rawLvl = DEFAULT_LVL_CONF_PARAMETERS
                self.gridSize = pygame.Rect(0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])  # explizit festlegen, da normalerweise gridSize on the fly berechnet wird

        else:
            DEBUG("Level.parse_lvl_file: kann .lvl-Datei nicht lesen. (existiert?, ist es eine Datei?", 1)
            rawLvl = DEFAULT_LVL_CONF_PARAMETERS
            self.gridSize = pygame.Rect(0, 0, DEFAULT_GRID_SIZE["X"], DEFAULT_GRID_SIZE["Y"])  # explizit festlegen, da normalerweise gridSize on the fly berechnet wird
        self.parameters["difficulty"] = rawLvl["difficulty"]
        self.parameters["title"] = rawLvl["title"]
        self.tileIDMap = rawLvl["grid"]
        self.gridSize = pygame.Rect(0, 0, len(rawLvl["grid"][0]), len(rawLvl["grid"]))
        DEBUG("Nutze zum Konfigurieren diese Werte: ", 11, rawLvl)
        DEBUG(".lvl-Parsing abgeschlossen", 1)
    # finde, lade und parse textureSetConf-File im übergebenen Verzeichnis in allTiles hinein

    def parse_texture_set(self):
        self.isParsed = False
        DEBUG("Level.parse_texture_set(levelPath)", 0)

        textureSetPath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
        DEBUG("öffne Textur Ordner an Pfad", 1, textureSetPath)
        if (os.path.isdir(textureSetPath) == False):  # wenn texturOrdner nicht exisitiert -> DEFAULT-Textur-Ordner
            DEBUG("TexturPfad nicht gefunden. falle auf DefaultTexturSet zurück...", 1, textureSetPath)
            textureSetPath = DEFAULT_TEXTURE_SET_PATH
            DEBUG("Falle auf DefaultTexturSet zurück...", 1, textureSetPath)
        textureSetConfRegex = os.path.join(textureSetPath, '') + '*.conf'
        DEBUG("suche nach confFiles mit diesem Ausdruck", 2, textureSetConfRegex)
        foundConfFilePaths = glob.glob(textureSetConfRegex)
        DEBUG("diese Files wurden gefunden", 10, foundConfFilePaths)
        if(len(foundConfFilePaths) > 0):
            if (foundConfFilePaths[-1] == "none"):  # wenn keine .conf-Datei gefunden -> DEFAULT-Textur-Ordner
                DEBUG("TexturPfad enthält keine Textur Datei/en(.conf).", 0, textureSetPath)
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
                    DEBUG("Datei getrimmt zu", 9, confData)
                    condition = TEXTURE_ID_BLOCK_REGEX
                    DEBUG("nutze zur Suche von ID-Blöcken folgenden RegEx-Ausdruck", 3, condition)
                    results = re.findall(condition, confData)
                    DEBUG(str(len(results)) + " gefundene ID-Blöcke:", 2)
                    DEBUG("gefundene ID Blöcke:", 8, results)
                    re.purge()
                    if (len(results) > 0):  # durchsuche jeden gefundenen ID Block
                        for idBlock in results:
                            rawParameters = DEFAULT_TILE_CONF_PARAMETERS.copy()
                            DEBUG("aktuell durchsuchter ID-Block", 2, idBlock)
                            for conditionName in DATA_CONDITIONS_TILE:
                                condition = DATA_CONDITIONS_TILE[conditionName]
                                DEBUG("Suche " + str(conditionName), 3)
                                DEBUG("Nutze den Regex Ausdruck '" + str(condition) + "'", 4)
                                resultsInBlock = re.findall(condition, idBlock)
                                DEBUG(str(len(resultsInBlock)) + " gefundene Elemente", 4)
                                DEBUG("Elemente:", 6, resultsInBlock)
                                if (len(resultsInBlock) > 0):
                                    if (conditionName == "ID"):
                                        x = resultsInBlock[0]
                                        x = x.replace("ID:", "")
                                        x = x.replace("{", "")
                                        DEBUG("ID-Wert ausgeschnitten", 6, x)
                                        rawParameters["ID"] = int(x)
                                        DEBUG("ID Wert " + str(rawParameters["groupID"]) + " eingefügt", 3)
                                    elif (conditionName == "groupID"):
                                        x = resultsInBlock[-1].replace("groupID=", "")
                                        DEBUG("groupID-Wert ausgeschnitten", 6, x)
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["groupID"] = int(x)
                                        DEBUG("groupID Wert " + str(rawParameters["groupID"]) + " eingefügt", 3)
                                    elif (conditionName == "isClippable"):
                                        x = resultsInBlock[-1].replace("isClippable=", "")
                                        DEBUG("isClippable-Wert ausgeschnitten", 6, x)
                                        DEBUG("nach umwandlung (bool)", 7, bool(int(x)))
                                        rawParameters["isClippable"] = bool(int(x))
                                        DEBUG("isClippable Wert " + str(rawParameters["isClippable"]) + " eingefügt", 3)
                                    elif (conditionName == "isAnimated"):
                                        x = resultsInBlock[-1].replace("isAnimated=", "")
                                        DEBUG("isAnimated-Wert ausgeschnitten", 6, x)
                                        DEBUG("nach umwandlung (bool)", 7, bool(int(x)))
                                        rawParameters["isAnimated"] = bool(int(x))
                                        DEBUG("isAnimated Wert " + str(rawParameters["isAnimated"]) + " eingefügt", 3)
                                    elif (conditionName == "dmgNeededToDestroy"):
                                        x = resultsInBlock[-1].replace("dmgNeededToDestroy=", "")
                                        DEBUG("dmgNeededToDestroy-Wert ausgeschnitten", 6, x)
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["dmgNeededToDestroy"] = int(x)
                                        DEBUG("dmgNeededToDestroy Wert " + str(rawParameters["dmgNeededToDestroy"]) + " eingefügt", 3)
                                    elif (conditionName == "damageOnCollision"):
                                        x = resultsInBlock[-1].replace("damageOnCollision=", "")
                                        DEBUG("damageOnCollision-Wert ausgeschnitten", 6, x)
                                        
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["damageOnCollision"] = int(x)
                                        DEBUG("damageOnCollision Wert " + str(rawParameters["damageOnCollision"]) + " eingefügt", 3)
                                    elif (conditionName == "damageOverTime"):
                                        x = resultsInBlock[-1].replace("damageOverTime=", "")
                                        DEBUG("damageOverTime-Wert ausgeschnitten", 6, x)
                                        
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["damageOverTime"] = int(x)
                                        DEBUG("damageOverTime Wert " + str(rawParameters["damageOverTime"]) + " eingefügt", 3)
                                    elif (conditionName == "layerID"):
                                        x = resultsInBlock[-1].replace("layerID=", "")
                                        DEBUG("layerID-Wert ausgeschnitten", 6, x)
                                        rawParameters["layerID"] = int(x)
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["layerID"] = int(x)
                                        DEBUG("layerID Wert " + str(rawParameters["layerID"]) + " eingefügt", 3)
                                    elif (conditionName == "playMvSlowDown"):
                                        x = resultsInBlock[-1].replace("playMvSlowDown=", "")
                                        DEBUG("playMvSlowDown-Wert ausgeschnitten", 6, x)
                                        DEBUG("nach umwandlung", 7, int(x))
                                        rawParameters["playMvSlowDown"] = int(x)
                                        DEBUG("playMvSlowDown Wert " + str(rawParameters["playMvSlowDown"]) + " eingefügt", 3)
                                    elif (conditionName == "playerMvManipulation"):
                                        x = resultsInBlock[-1].replace("playerMvManipulation=", "")
                                        DEBUG("playerMvManipulation-Wert ausgeschnitten", 6, x)
                                        temp = x.split(",")
                                        if (len(temp) >= 2):
                                            temp[0] = int(temp[0].replace("[", ""))
                                            temp[1] = int(temp[1].replace("]", ""))
                                        else:
                                            DEBUG("ausgelesene Liste hat zu wenig elemente, fallback auf default",6, temp)
                                            temp = DEFAULT_TILE_CONF_PARAMETERS["playerMvManipulation"]
                                        DEBUG("nach umwandlung", 7, temp)
                                        rawParameters["playerMvManipulation"].clear()
                                        rawParameters["playerMvManipulation"].append(temp[0]) 
                                        rawParameters["playerMvManipulation"].append(temp[1]) # wandle die ersten beiden elemente von temp in ints um
                                        DEBUG("playerMvManipulation Wert  eingefügt", 3, rawParameters["playerMvManipulation"])
                                    elif (conditionName == "preferredNeighborIDs"):
                                        x = resultsInBlock[-1].replace("preferredNeighborIDs=", "")
                                        DEBUG("preferredNeighborIDs-Wert ausgeschnitten. Nutze " + str(x) + "zur Extraktion der Werte", 6)
                                        firstSplit = x.split("][")
                                        DEBUG("erster split bei ][", 7, firstSplit)
                                        neighbors = []
                                        for split in firstSplit:
                                            neighbors.append(list())
                                            DEBUG("Betrachte Element " + str(split), 8)
                                            split = split.replace("[[", "")
                                            split = split.replace("]]", "")
                                            DEBUG("Element getrimmt zu " + str(split), 8)
                                            secondSplit = split.split(",")
                                            DEBUG("Splitte Element zu", 8, secondSplit)
                                            if (len(secondSplit) == 3):
                                                neighbors[-1] = secondSplit
                                                for i in range(0, len(neighbors[-1])):
                                                    neighbors[-1][i] = int(neighbors[-1][i])
                                                    DEBUG("wert " + str(neighbors[-1][i]) + "eingelesen(int)", 9)
                                        if (len(secondSplit) == 3):
                                            rawParameters["preferredNeighborIDs"] = neighbors 
                                            DEBUG("PreferredNeighbors eingelesen", 3, rawParameters["preferredNeighborIDs"])
                                        else:
                                            DEBUG("preferredNeighbor konnte nicht eingelesen werden (längen korrekt?), nutze default-Werte", 3)
                                else:
                                    if(conditionName == "groupID"):
                                        DEBUG("Es wurde keine GroupID gefunden", 3)
                                re.purge()
                            DEBUG("füge neues TileID-Objekt der Liste hinzu", 2, rawParameters)
                            self.parsedTileIDs.append(rawParameters)
                    else:
                        DEBUG("keine ID Blöcke gefunden, überspringe Datei", 2)
                else:
                    DEBUG(".conf Datei leer?, überspringe diese Datei", 2)

            self.isParsed = True
        else:
            DEBUG("es wurden keine textur-Configs gefunden!!, alle geladenen Blöcke die != 0 sind werden einfarbig", 1)
        if(len(self.parsedTileIDs) <= 0):
            DEBUG("Es wurden keine Tile IDs gefunden!!, alle geladenen Blöcke die != 0 sind werden einfarbig", 1)
        else:
            DEBUG("Es wurden " + str(len(self.parsedTileIDs)) + " Tile-Parameter eingelesen")
    # 1. lade textureSetConf und beschreibe sämtliche geladenen Tiles mit den zu GroupID entsprechenden Eigenschaften
    # 2. wähle im 2. Schritt die passende TileID(entsprechend der Neighbors) aus der geöffneten Gruppe aus
    # 3. erstelle ein tile und übergebe den texturepfad des entsprechenden tiles
    # das bild wird erst mit build() geladen um zu verhindern dass alle lvl parallel offen sind
#Es sollte am besten in compile die am besten passende ID ermittelt werden
#die könnte in dem Grid gespeichert werden als dict{groupID, tileID}
    def parse(self):
        if (not self.isParsed):

            DEBUG("Level.parse()", 1)
            DEBUG("rufe parse_lvl_file() auf", 2)
            self.parse_lvl_file()
            DEBUG("rufe parse_texture_file() auf", 2)
            self.parse_texture_set()
            DEBUG("Parsing abgeschlossen", 1)
            self.isParsed = True

            #to be removed (when compile is finished)
            self.isCompiled = True
        else:
            DEBUG("Level ist bereits geparst", 1)
    
    def compile(self):
        DEBUG("level.compile():", 1)
        if(not self.isCompiled):
            if (not self.isParsed):
                DEBUG("Level ist noch nicht geparst. rufe LevelParsing auf...", 2)
                self.parse()
            else:
              self.currentTilePos["X"] = 0
            self.currentTilePos["Y"] = 0
            DEBUG("betrachte TileMap:", 12, self.tileIDMap)
            temp = 0
            for y in self.tileIDMap:
                DEBUG("betrachte Zeile: " + str(self.currentTilePos["Y"]), 2)
                for x in y:
                    DEBUG("betrachte Spalte: " + str(self.currentTilePos["Y"]), 3)
                    # suche hier nach den nachbarn und der aktuellen position
                    DEBUG("erstelle Liste mit direkten Nachbarn", 4)
                    neighbors = self.get_neighbors(self.currentTilePos)
                    matchingTileConfs = []
                    DEBUG("durchsuche TileConfs nach Tiles mit groupID == " + str(x), 4)
                    for TileConf in self.parsedTileIDs:
                        if (TileConf["groupID"] == x):
                            matchingTileConfs.append(TileConf)
                    DEBUG( str(len(matchingTileConfs)) + " übereinstimmende TileConfs gefunden", 5)
                    DEBUG("vergleiche Nachbarn in allen gefundenen TileConfs mit zuvor erstellter Nachbar-Liste...", 4)
                    debugCounter = 0
                    foundMatches = []
                    for TileConf in matchingTileConfs:
                        debugCounter += 1
                        DEBUG("vergleiche " +  str(debugCounter) + "/" + str(len(matchingTileConfs)), 5)
                        # rufe matchNeighbors auf und übergebe TileConf[neighbors] und self.getNeighbors(x)
                        matches = self.match_neighbors(TileConf["preferredNeighborIDs"], self.get_neighbors(self.currentTilePos))
                        if (matches != None):
                            DEBUG("Match mit " + str(len(matches)) + " Übereinstimmungen gefunden", 6)
                            DEBUG("Es handelt sich um TileID " + str(TileConf["ID"]), 7)
                            # if(len(tileAndMatch["matches"]) < len(matches)):
                            foundMatches.append({"TileConf": TileConf, "matches": len(matches)})
                        else:
                            DEBUG("keine Übereinstimmungen gefunden", 6)
                        # sortiere Liste nach enthaltenen 'matchesAttributen'
                    
                    if(len(foundMatches) > 0):
                        sortedMatchingTileConfs = sorted(foundMatches, key = lambda i: i['matches'],reverse=True) 
                        DEBUG("Match-Liste nach Sortierung:", 12, sortedMatchingTileConfs)
                        bestMatch = sortedMatchingTileConfs.pop(0)["TileConf"]
                        DEBUG("Als bestes Match wurde TileID " + str(bestMatch["ID"]) + " gewählt", 4)
                    else:
                        DEBUG("matchesListe ist leer, nutze stattdessen eine beliebige ID aus aus der Gruppe " + str(TileConf["groupID"]) + " zu nutzen", 4)
                        if(len(matchingTileConfs) > 0):
                            bestMatch = matchingTileConfs[0]
                        else:
                            DEBUG("es gibt überhaupt keine Tiles mit übereinstimmender groupID = " + str(TileConf["groupID"]), 5)
                            DEBUG("wähle beliebiges Tile aus der TileConfs-Liste", 5)
                            if(len(self.parsedTileIDs) > 0):
                                bestMatch = self.parsedTileIDs[0]
                            else:
                                DEBUG("Es scheinen überhaupt keine TileConfs vorhanden zu sein, wähle stattdessen DEFAULT-Conf", 6)
                                bestMatch = DEFAULT_TILE_CONF_PARAMETERS
        #speichere bestMatch in temporärer tileIDMap und überschreib diese bei abschluss des compileVorgangs.
        #verwerfe Liste bei schweren Fehlern
        

    def uncompile(self):
        #wandelt die dict-Objekte zurück in groupIDs
        #setze zurück auf isCompiled = False
        pass

    # 1. ließt alle tileIDs ein und lädt jewils die entsprechende textur
    # 2. erstelle eine sprite.group mit sämtlichen tiles, passiven tiles, animierten tiles,
    # wenn IS_BUILD_ON_UPDATE = True, dann wird mit jedem build aufruf nur ein tile erstellt und currentTilePos auf dieses gesetzt.
    # (überprüfen lässt sich der aktuelle Build-Zustand mit bool self.isBuild())
    # gibt eine Liste mit übereinstimmungen
    def match_neighbors(self, neighbors1=[], neighbors2=[]):
        DEBUG("Level.match_neighbors(self, neighbors1 = [], neighbors2 = []):", 5)
        matches = []
        position = {"X": 0, "Y": 0}
        match = {"position": {}, "groupID": 0}
        if (len(neighbors1) == 3 & len(neighbors2) == 3):
            for list in neighbors1:
                if (len(list) == 3 & len(neighbors2[position["Y"]]) == 3):
                    for element in list:
                        DEBUG("vergleiche Element an Position", 7, position)
                        if (element == neighbors2[position["Y"]][position["X"]]):
                            DEBUG("Match gefunden an", 8, position)
                            matches.append({"position": position, "groupID": element})
                        position["X"] += 1
                    position["X"] = 0
                    position["Y"] += 1
                else:
                    DEBUG("Eine der Listen in einer der übergebenen Listen hat eine unerwartete Länge", 5)
                    return None
            DEBUG( str(len(matches)) + " gefundene Matches:", 6)
            DEBUG( str(len(matches)) + " ListenInhalt:", 9, matches)
            return matches
        else:
            DEBUG("Eine der übergebenen Listen hat eine unerwartete Länge", 5)
            return None

    # Berechne Größe eines einzelnen TIles und gebe ein entsprechendes Rect Objekt zurück (x und y = 0)
    def calc_tileSize(self):
        return pygame.Rect(0, 0, ARENA_AREA.width // self.gridSize.w, ARENA_AREA.h // self.gridSize.h)

    # baut die Spieloberfläche mit sämtlichentiles auf
    def build(self):
        if (self.isCompiled):
            DEBUG("Level.build():", 0)
            if (IS_BUILD_ON_UPDATE):
                DEBUG("IS_BUILD_ON_UPDATE ist aktiv", 1, IS_BUILD_ON_UPDATE)
                if (self.tile_exists(self.currentTilePos)):
                    pass
            else:
                DEBUG("IS_BUILD_ON_UPDATE ist inaktiv", 1, IS_BUILD_ON_UPDATE)
                
                
                
                
                
                
                
                #wird in compile ausgelagert!-------------------------------------------------------------------------------
                self.currentTilePos["X"] = 0
                self.currentTilePos["Y"] = 0
                DEBUG("betrachte TileMap:", 12, self.tileIDMap)
                temp = 0
                for y in self.tileIDMap:
                    DEBUG("betrachte Zeile: " + str(self.currentTilePos["Y"]), 2)
                    for x in y:
                        DEBUG("betrachte Spalte: " + str(self.currentTilePos["Y"]), 3)
                        # suche hier nach den nachbarn und der aktuellen position
                        DEBUG("erstelle Liste mit direkten Nachbarn", 4)
                        neighbors = self.get_neighbors(self.currentTilePos)
                        matchingTileConfs = []
                        DEBUG("durchsuche TileConfs nach Tiles mit groupID == " + str(x), 4)
                        for TileConf in self.parsedTileIDs:
                            if (TileConf["groupID"] == x):
                                matchingTileConfs.append(TileConf)
                        DEBUG( str(len(matchingTileConfs)) + " übereinstimmende TileConfs gefunden", 5)
                        DEBUG("vergleiche Nachbarn in allen gefundenen TileConfs mit zuvor erstellter Nachbar-Liste...", 4)
                        debugCounter = 0
                        foundMatches = []
                        for TileConf in matchingTileConfs:
                            debugCounter += 1
                            DEBUG("vergleiche " +  str(debugCounter) + "/" + str(len(matchingTileConfs)), 5)
                            # rufe matchNeighbors auf und übergebe TileConf[neighbors] und self.getNeighbors(x)
                            matches = self.match_neighbors(TileConf["preferredNeighborIDs"], self.get_neighbors(self.currentTilePos))
                            if (matches != None):
                                DEBUG("Match mit " + str(len(matches)) + " Übereinstimmungen gefunden", 6)
                                DEBUG("Es handelt sich um TileID " + str(TileConf["ID"]), 7)
                                # if(len(tileAndMatch["matches"]) < len(matches)):
                                foundMatches.append({"TileConf": TileConf, "matches": len(matches)})
                            else:
                                DEBUG("keine Übereinstimmungen gefunden", 6)
                            # sortiere Liste nach enthaltenen 'matchesAttributen'
                        
                        if(len(foundMatches) > 0):
                            sortedMatchingTileConfs = sorted(foundMatches, key = lambda i: i['matches'],reverse=True) 
                            DEBUG("Match-Liste nach Sortierung:", 12, sortedMatchingTileConfs)
                            bestMatch = sortedMatchingTileConfs.pop(0)["TileConf"]
                            DEBUG("Als bestes Match wurde TileID " + str(bestMatch["ID"]) + " gewählt", 4)
                        else:
                            DEBUG("matchesListe ist leer, nutze stattdessen eine beliebige ID aus aus der Gruppe " + str(TileConf["groupID"]) + " zu nutzen", 4)
                            if(len(matchingTileConfs) > 0):
                                bestMatch = matchingTileConfs[0]
                            else:
                                DEBUG("es gibt überhaupt keine Tiles mit übereinstimmender groupID = " + str(TileConf["groupID"]), 5)
                                DEBUG("wähle beliebiges Tile aus der TileConfs-Liste", 5)
                                if(len(self.parsedTileIDs) > 0):
                                    bestMatch = self.parsedTileIDs[0]
                                else:
                                    DEBUG("Es scheinen überhaupt keine TileConfs vorhanden zu sein, wähle stattdessen DEFAULT-Conf", 6)
                                    bestMatch = DEFAULT_TILE_CONF_PARAMETERS
                        #-------------------------------------------------------------------------------wird in compile ausgelagert!
                        
                        
                        
                        
                        
                        # Wir haben jetzt die exakte tileID n self.currentPosition {X,Y}
                        # -ermittle die größe eines einzelnen tiles OK
                        # -ermittle die Pixel-Position des ektuellen tiles mit
                        # currentPos[X] * tileSize.w
                        DEBUG("Berechne Daten für neues Tile-Element:", 3)
                        tileRect = self.calc_tileSize()
                        tileRect.x = self.currentTilePos["X"] * tileRect.w
                        tileRect.y = self.currentTilePos["Y"] * tileRect.h
                        DEBUG("X-Position   = " + (str(tileRect.x)), 4)
                        DEBUG("Y-Position   = " + (str(tileRect.y)), 4)
                        DEBUG("Breite       = " + (str(tileRect.w)), 4)
                        DEBUG("Höhe         = " + (str(tileRect.h)), 4)
                        tileTexturePath = os.path.join(os.path.dirname(self.parameters["levelFilePath"]), "texture", "tiles")
                        DEBUG("Textur-Pfad: = " + tileTexturePath, 4)
                        DEBUG("Parameter=", 5, bestMatch)
                        newTile = Tile.Tile(tileRect, tileTexturePath, bestMatch)
                        if (newTile.has_animation()):
                            self.animatedTiles.add(newTile)
                        if (newTile.has_damage()):
                            self.damagingTiles.add(newTile)
                        if (newTile.has_collision()):
                            self.collidableTiles.add(newTile)
                        self.currentTilePos["X"] += 1  # wird benötigt um entsprechende Position des tiles zu bestimmen
                    self.currentTilePos["X"] = 0
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
