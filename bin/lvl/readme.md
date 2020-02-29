# Beschreibung der Level

Ein Level ist ein 2 Dimensionales Array mit einem int als Inhalt.
Dieser Integer bestimmt, ob sich an dieser Position ein Tile befindet oder nicht, und was fr ein tile sich da befindet.
Diese TileIDs bestimmen, welche TexturListe genutzt wird. viele Texturen haben verschiedene Varianten mit verschiedenen Seiten, die Variante wird von den Nachbarn im Lvl-Raster bestimmt.

## Verteilung der TileIDs

    [-X] - [-1]    <      0      <     [1] - [X]
[clipping_erlaubt] < [kein_tile] < [clipping_verboten]

- 51-100 tiles mit Schaden
- 1-50 tiles ohne Schaden
- 0 = leer (kein Tile)
- [-1] - [-50] = tiles ohne Schaden
- [-51] - [-100] = tiles mit Schaden

texturen und Schaden unterscheiden sich je ID.
Ablauf bei unzuordbaren IDs:

1. wenn eine ID nicht in tiles-Ordner gefunden wird, wird im defaultTilesOrdner nach einer passenden gesucht...
2. wenn da auch keine passende Textur gefunden wird,dann wird nach einem ähnlichen tile in den levelTiles gesucht...
3. Wenn auch hier kein tile gefunden wird, wird das selbe nocheinmal mit den defaultTiles versucht...
4. Wenn dies auch fehlschlägt, dann wird das tile zu ID=0 (leeres tile) geändert...

>(Es wird nach IDs gesucht, die ähnliche Eigenschaften haben. Da wir nur Schaden, kein Schaden, cliiping_erlaubt und clipping_nicht_erlaubt wird einfach geschaut ob es >tiles im selben ID bereich gibt und das von der Entfernung nächste wird genommen)
