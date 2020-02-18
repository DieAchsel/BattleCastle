#Classe für die spielbaren Spielfigur
class Fighter:
    __name__ = "Fighter"

    posX = int()
    posY = int()
    health = int()


    def __init__(self, posx, posy):
        self.posX = posx
        self.posY = posy
        self.health = 100

#    def goLeft(self):


#    def goRight(self):


#    def jump(self):