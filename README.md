# Sparda Bank (Südwest) Kontoauszüge PDF - Dateien zu CSV (Homebank)

**Dies ist kein offizielles Programm der Sparda Bank Südwest**

Motivation
-------------
Das regelmäßige Abrufen der Kontoauszüge ist mir meist zu Zeit aufwendig, gerade auch wegen der PSD2.

Daher möchte ich über Homebanking in jährlichen Abständen die Archive herunterladen und in Programme wie [Homebank](http://homebank.free.fr/en/index.php) importieren.

Leider liegen die Archive nur als PDF - Dateien vor.  Daher wurde dieses Programm entwickelt, das Kontoauszüge als PDF einliest und in CSV umwandelt.

Abhängigkeiten
--------------------
Zum Umwandeln von PDF zu Text verwende ich:

* [pdfminer](https://github.com/pdfminer/pdfminer.six/) 

Dieser ist normalerweise in jeder Linux Distri mit an Board:

ArchLinux / Manjaro
`pacman -Sy community/python-pdfminer`

Debian
`apt install -y python3-pdfminer`

Installation
-------------
Wenn die Abhängigkeit installiert ist, reicht eigentlich nur noch

```
git clone https://github.com/h8h/convertSpardaKontoauszugToCSV.git

cd convertSpardaKontoauszugToCSV

./init.py kontoauszug.pdf

oder

./init.py *pdf

```

Bekannte Probleme
-----------------
Das PDF ist oftmals nicht sauber gegliedert, daher kann es zu Konflikten kommen.

Dennoch hat Das Programm meine über 20 Kontoauszüge von 01.01.2019 - 30.09.2020 problemlos umgewandelt.

Es beherrscht die alten Versionen wie auch die Neuen.

**Trotzdem** schließe ich umfassend die Garantie der Funktionsweise aus! Ich übernehme keinerlei Haftung für eventuelle Schäden.

Bitte überprüft das das CSV die korrekten Buchungen erhält.

Beispielsweise schaue ich mir immer die Kontostände vorher und nacher an und vergleiche ob diese übereinstimmen.

Lizenz
------
Siehe LICENSE - Datei und die von [pdfminer](https://github.com/euske/pdfminer).
