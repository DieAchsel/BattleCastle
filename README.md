# BattleCastle

> Dies ist eine Ausarbeitung für den Kurs _Skriptsprachen 2019_ der **Fachhochschule Südwestfalen**.
> Die Ersteller und Eigentümer dieses Projektes sind **Alex Schäfer** und **Nils Liefländer**.

## Einführung

Dies ist ein Geschicklichtkeitsspiel, in dem 2 Spieler in einem vertikalen labyrinth gegeneinander kämpfen.
Die beiden Spieler können in dem Labyrinth emporspringen um Deckung zu finden oder ein besseres Schussfeld zu erhalten.
Es sind Healpacks um Labyrinth verteilt.

<object data="/Dokumentation/Klassendiagramm.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="/Dokumentation/Klassendiagramm.pdf">
        <p>PDF kann nicht angezeigt werden. Hier öffnen: <a href="/Dokumentation/Klassendiagramm.pdf">Klassendiagramm</a>.</p>
    </embed>
</object>

## Spielfeld

Das Spielfeld ist in ein Raster aufgeteilt, nach welchem sich der Levelaufbau orientiert, nicht jedoch der Spieler.
Ist das Raster an den Rändern geöffnet (keine blockierenden Objekte im weg), dann ist es möglich von z.B. der rechten seite rechts rau auf die Linke Seite zu laufen, genauso wird mit der Y-Achse verfahren.
Wenn jedoch die offene Seite von einem Objekt an der äquivalenten unteren Stelle blockiert werden, dann sind für den RandTile collisionen aktiv
<object data="/Dokumentation/Oberfl%C3%A4che.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="/Dokumentation/Oberfl%C3%A4che.pdf">
        <p>PDF kann nicht angezeigt werden. Hier öffnen: <a href="/Dokumentation/Oberfl%C3%A4che.pdf">Spielfeld</a>.</p>
    </embed>
</object>

## Bedienung

Die Bedienung ist sehr einfach gehalten.
Standardmäßig haben 2 Spieler bereits eine vordefinierte Tastenbelegung:
<object data="/Dokumentation/Steuerung.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="/Dokumentation/Steuerung.pdf">
        <p>PDF kann nicht angezeigt werden. Hier öffnen: <a href="/Dokumentation/Steuerung.pdf">Steuerung</a>.</p>
    </embed>
</object>

Es können weitere Spieler hinzugefügt werden. Diese benötigen, wenn mit der Tastatur gespielt wird, jedoch je weiteren Spieler eine Zusätzliches KeyMapping
Dies kann (in Zukunft) über das Menü erstellt werden. (Aktuell muss das mapping in der playerCFG.py hinzugefügt werden)

Wenn über die Spieleigenen Controller gespielt wird, ist diese Beschränkung nicht mehr vorhanden, da jeder Controller über den jeweiligen seriellen Port erkannt wird.

## Installation

Das Spiel benötigt verschiedene Module die nicht im Standard-Package enthalten sind.
Die fehlenden Module lassen sich jedoch sehr einfach mit pip installieren.
Eine Liste sämtlicher verwendeter Module findet sich in requirements.txt
<object data="/requirements.txt" type="application/pdf" width="700px" height="700px">
    <embed src="/requirements.txt">
        <p>txt kann nicht angezeigt werden. Hier öffnen: <a href="/requirements.txt">Abhängigkeiten</a>.</p>
    </embed>
</object>
Weitere Installations-Schritte sind nicht notwendig.

## Quellen

in dem Quellenverzeichnis lassen sich die für die Implementierung hinzugezogenen Quellen nachvollziehen:
<object data="/Dokumentation/Quellen.txt" type="application/pdf" width="700px" height="700px">
    <embed src="/Dokumentation/Quellen.txt">
        <p>PDF kann nicht angezeigt werden. Hier öffnen: <a href="/Dokumentation/Quellen.txt">Quellen</a>.</p>
    </embed>
</object>



### überschr3

...

*kursiv*

_kursiv_

~~durchgestrichen~~

**fett und _kursiv_**

__fett__

**fett**


[Linkname](http://www.adresse.com)

[relativer link](../blob/master/LICENSE)

>kommentar

`Quellcode so schreiben`

das ist ein logo:![alt logo](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")



| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

Ich bin auch dabei :)
test
