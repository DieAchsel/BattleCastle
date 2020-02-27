# Beschreibung der Level

Ein Level ist ein 2 Dimensionales Array mit einem int als Inhalt.
Dieser Integer bestimmt, ob sich an dieser Position ein Tile befindet oder nicht, und was fr ein tile sich da befindet.
Diese TileIDs bestimmen, welche TexturListe genutzt wird. viele Texturen haben verschiedene Varianten mit verschiedenen Seiten, die Variante wird von den Nachbarn im Lvl-Raster bestimmt.
TileIDs:

- 1 = defaultTile
- 0 = leer (kein Tile)
- -1 = LavaTile
- -2 = rockFormationTile
- ... (in Zukunft zu erweitern)
