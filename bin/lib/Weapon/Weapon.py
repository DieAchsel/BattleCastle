from bin.lib.Projectile import Projectile
#ZURÜCKGESTELLT:
#Zur Abgabe wird legiglich ein einfacher, statisch programmierter Meele-Attack implementiert
#für den Ausblick in die Zukunft folgt unten eine grobe Beschreibung der Weapon-Klasse

#hier werden in Zukunft Waffen eingebaut:



#-Eine Waffe besteht aus einer Surface, auf die eine Waffentextur gezeichnet wird
#-Das Zielen nach oben und unten wird mit der rotation der weapon-surface realisiert.
#in der weapon.conf (darf mehrere weapon.confs geben) stehen die Eigenschaften der einzelnen Waffen inklusive:
#welche Projektile werden genutzt?
#Wo ist die Waffenmündung? (an dieser Stelle werden die Projektile initialisiert)
#wie groß ist die Waffe (gr.-verhältnis zu spieler (Spieler und Waffen werden entsprechen der map-größe skaliert))



#(wenn in Zukunft pro projektiltyp eine eigene childKlasse implementiert wird, werden die Projektil-Parameter wie (geschwindigkeit, damage,...) in der Weapon.conf gespeichert)
#Wenn nur eine Projektilklasse implementiert wird, werden die Projektil-Parameter in einer/mehreren projectile.conf gespeichert