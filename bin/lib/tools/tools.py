import os, re
#from bin.config.generalCFG import GAME_DIR
#gibt eine Liste mit pasenden Pfaden
def regExFileFinder(filePath = "", regex = ".*", recursive = False, justFiles = False):
    if(regex == ""):
        regex = ".*"
    if(not os.path.exists(filePath)):
        #print("Pfad " + str(filePath) + " existiert nicht")
        #filePath = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        #hier in Zukunft direkt eine leere Liste übergeben (dateien aus irgendeinem Pfad kann man nicht gebrauchen)
        return []
    else:
        if(os.path.isdir(filePath)):
            print(filePath)
            directory = os.listdir(filePath)
            newDirectory = []
            for x in directory:
                if(justFiles):
                    if(os.path.isfile(x)):
                        if(x[0] != "."):
                            newDirectory.append(x)
                else:
                    if(x[0] != "."):
                            newDirectory.append(x)
            directory.clear()
            directory = newDirectory
            #print(directory)#DEBUG-Meldung noch entfernen
            allResults = []
            try:
                for x in directory:
                    #print("Prüfe " + str(x))
                    results = re.findall(regex, x)
                    #print("    Anzahl an Matches " + str(len(results)) + ": " + str(results))
                    if(len(results) > 0):
                        allResults.append(x)
                return allResults
            except:
                print("ungültiger Ausdruck")
                return []
#gibt eine Liste in vom Menschen lesbarer Form als String-Liste zurück, mit top kann eine maximalAnzahl an anzuzeigenden Items festgelegt werden
def listPrinter(list = None, top = -1):
    convertedList = []
    if(list != None):
        try:
            tabs = "    "
            counter = 0
            convertedList.append("Listen-Länge: " + str(len(list)))
            #print(convertedList[-1])
            #convertedList.append("Inhalt:")
            #print(convertedList[-1])
            for item in list:
                counter += 1
                if(top >= counter):
                    convertedList.append(tabs + "Item " + ("{:0" + str(len(str(len(list)))) +"d}").format(counter) + ": '" + str(item).replace("\n", "") + "'")
                    #print(convertedList[-1])
                elif(top == counter - 1):
                    convertedList.append(tabs + "...(" + str(len(list) - top) + " weitere Items ausgeblendet)")
                    #print(convertedList[-1]) 
                elif(top < 0):
                    convertedList.append(tabs + "Item " + ("{:0" + str(len(str(len(list)))) +"d}").format(counter) + ": '" + str(item).replace("\n", "") + "'")
            return convertedList
        except:
            print("listPrinter(results=[], top = -1): Es ist ein Fehler aufgetreten. Ist list iterierbar?")
            return ["Liste konnte nicht erstellt werden"]
    else:
        return []

def dictPrinter(dict = None, top = -1):
    convertedList = []
    if(dict != None):
        #try:
            tabs = "    "
            counter = 0
            convertedList.append(str(len(dict)) + " Einträge im Dictionary")
            #print(convertedList[-1])
            #convertedList.append("Inhalt:")
            #print(convertedList[-1])
            space = ""
            for item in dict:
                counter += 1
                if(top >= counter):
                    line = tabs + "Eintrag " + ("{:0" + str(len(str(len(dict)))) +"d}").format(counter) + ":  '" + str(item) + "'" + space + ":    " + str(dict[item])
                    convertedList.append(line)
                    #print(convertedList[-1])
                elif(top == counter - 1):
                    convertedList.append(tabs + "...(" + str(len(list) - top) + " weitere Einträge ausgeblendet)")
                    #print(convertedList[-1]) 
                elif(top < 0):
                    line = tabs + "Eintrag " + ("{:0" + str(len(str(len(dict)))) +"d}").format(counter) +":  '" + str(item) + "'" + space + ":    " + str(dict[item])
                    convertedList.append(line)
            return convertedList
        #except:
            #print("dictPrinter(results=[], top = -1): Es ist ein Fehler aufgetreten. Ist dict iterierbar?")
            #return ["Liste konnte nicht erstellt werden"]
    else:
        return []

def test_dictPrinter():
    testDict = {"Key1": "value1",
                "Key2": 2,
                "Key3": [3,3,3],
                "Key4": {"4": "vier"},
                "Key5": "value5",
                "Key6": "value6",
                "Key7": "value7",
                "Key8": "value8",
                "Key9": "value9",
                "Key10": "value10",
                "Key11": 11,
                "Key12": 12,
                "Key13": 13,
                "Key14": "value14",
                "Key15": "value15",}
    result = dictPrinter(testDict)
    for x in result:
        print(x)

#Testet einen eingegebenen RegEx Ausdruck und gibt das Ergebnis aus
def regExTester(filePath = ""):
    print("dieses Tool vergleicht den Verzeichnis-Inhalt von\n" + filePath + "\nmit dem eingegebenen regEx-Ausdruck und gibt die Ergebnisse als Liste aus.")
    while(True):
        print("regulären Ausdruck eingeben:")
        result = listPrinter(regExFileFinder(filePath, input(), justFiles = False))
        for x in result:
            print(x)
#test_dictPrinter()
regExTester(os.path.join("bin", "lvl", "000", "texture", "tiles"))


#Debugging-Tool

#in Zukunft in debugKlasse umwandeln
DEBUG_ENABLED = False
DEBUG_LEVEL = 5
DELAY_ON_DEBUG = 0 #gibt ein Delay in s (darf float sein) an, wie lang nach jeder DEBUGGING-Nachricht gewartet werden soll.
ON_DEBUG_USER_CONTINUES = False #wenn ein kontinueKey (pygame.event) angegeben ist, wird bis zur Eingabe von Enter gewartet.

LOG_FILE = False
#Wenn DEBUG_ENABLED, dann gib Debuggingmeldungen aus, je nach lvl mit angepasstem Detail
#wie detailliert sollen die Meldungen sein. bei DEBUG_LEVEL >= 12 wird je nach integrierung jede Daten-Transaktion in der Konsole ausgegeben
#Debugging-Funktion:
logOpened = bool
if(LOG_FILE & DEBUG_ENABLED):
    logFile = open(os.path.join(GAME_DIR, "DEBUG.log"), 'a')
else:
    logFile = None
def debug_logger(msg = "Meldung ohne Inhalt", debugLevel = 0, ObjectToPrint = None, LogInFile = True):
    #from self import logOpened, logFile
    if(DEBUG_ENABLED):  
        spacing = ""  
        tabs = "    " 
        output_prefix = "TEST_DEBUGGING: " + time.strftime("%H:%M:%S") + "   "
        output = []    
        for x in range(debugLevel): #Rücke Meldungen in tieferem Layer ein
            spacing += tabs
        output.append(output_prefix + spacing + msg)
        if(ObjectToPrint != None): 
            if type(ObjectToPrint) is list:
                converted = listPrinter(ObjectToPrint)
                for x in converted:
                    output.append(output_prefix + spacing + tabs + x)
            elif type(ObjectToPrint) is dict:
                converted = dictPrinter(ObjectToPrint)
                for x in converted:
                    output.append(output_prefix + spacing + tabs + x)
            else:
                output.append(output_prefix + spacing + tabs + str(ObjectToPrint))
        if(debugLevel <= DEBUG_LEVEL):     
            if(DELAY_ON_DEBUG > 0):
                time.sleep(DELAY_ON_DEBUG)
            if(ON_DEBUG_USER_CONTINUES):
                output.append(output_prefix + spacing + tabs + "Nutzer-Eingabe: '" + input() + "'")
            for x in output:
                print(x)
                if(LOG_FILE & LogInFile):
                    logFile.write((x + "\n"))
                    logFile.flush()