#baut die Map
from bin.src.classPlayer import Fighter

def buildMap():
    char1 = Fighter(200, 500)
    char2 = Fighter(500, 500)
    return (char1,char2)