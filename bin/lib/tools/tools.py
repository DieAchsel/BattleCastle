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
            convertedList.append("Inhalt:")
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
            print("listPrinter(results=[], top = -1): Es ist ein Fehler aufgetreten. Ist results iterierbar?")
            return ["Liste konnte nicht erstellt werden"]
    else:
        return []

#Testet einen eingegebenen RegEx Ausdruck und gibt das Ergebnis aus
def regExTester(filePath = ""):
    print("dieses Tool vergleicht den Verzeichnis-Inhalt von\n" + filePath + "\nmit dem eingegebenen regEx-Ausdruck und gibt die Ergebnisse als Liste aus.")
    while(True):
        print("regulären Ausdruck eingeben:")
        result = listPrinter(regExFileFinder(filePath, input(), justFiles = False), top = 7)
        for x in result:
            print(x)

#regExTester()

