
---

ImagesExtract2

Projektbeschreibung

ImagesExtract2 ist ein modulares Bildverarbeitungssystem, das in drei Hauptphasen unterteilt ist:

1. Initialisierung


2. Datenvorbereitung


3. Spelling-gesteuerte Bildverarbeitung



Das Ziel des Projektes ist es, eine große Menge an Bilddateien effizient zu verarbeiten, strukturiert abzulegen und flexibel mit verschiedenen Nachbearbeitungsskripten weiterzuverarbeiten.


---

Ablaufübersicht

Das Programm wird vollständig über ein zentrales Startskript gestartet und verwaltet seine Arbeit in klar getrennten Modulen.

Hier die grafische Flussdarstellung des gesamten Ablaufs:
Verstanden.
Ich gebe dir jetzt die komplette Projekt-Aufbauübersicht nur in ASCII, ohne Unicode-Boxen oder Sonderzeichen.
Technisch, klar, perfekt für Readme oder Doku.

Hier die ASCII-Version:


```plaintext
---

ImagesExtract2/
|
|-- moduls/
|    |-- folders.py         # Erstellt und verwaltet die Basis-Ordnerstruktur
|    |-- logger.py          # Globale Fehler- und Statusprotokollierung
|    |-- utils.py           # Arbeitsverzeichnis und Pfadmanagement
|
|-- settings/
|    |-- start.json         # Konfiguration: Arbeitsverzeichnis, allgemeine Optionen
|    |-- foldes.json        # Konfiguration: Ordnerstruktur
|    |-- spelling.json      # Konfiguration: Steuerung der Nachbearbeitungsskripte
|
|-- spelling/
|    |-- PrepareInput.py    # Sortiert Eingabebilder nach Formaten (01_png, 01_webp, etc.)
|    |-- Converter.py       # Konvertiert Bilder ins Zielformat und verteilt sie
|    |-- Spelling.py        # Steuert Ausführung der Bearbeitungsskripte auf bestimmten Ordnern
|    |-- Enhancement.py     # Modul für Bildverbesserung
|    |-- Extract.py         # Modul für Objektextraktion
|    |-- ExtractGray.py     # Modul für Graustufenextraktion
|    |-- TransBack.py       # Modul für Hintergrundtransparenz
|    |-- SwapColors.py      # Modul für Farbtausch
|    |-- CleanUp.py         # Modul für Bildaufräumarbeiten
|    |-- Scal.py            # Modul für Bildskalierung
|    |-- Collation.py       # Modul für Zusammenfassung der Ergebnisse
|    |-- invert.py          # Modul für Farbinvertierung
|
|-- startskript.py          # Hauptstartpunkt des Programms, steuert Initialisierung und Ablauf
|-- README.md               # Projektbeschreibung und Dokumentation
|-- requirements.txt        # (optional) Python-Abhängigkeiten für Installation
|
|-- log.txt                 # Laufende Protokollierung
|-- error_log.txt           # Fehlerprotokollierung
|-- InContent.txt           # (optional) weitere Metadaten oder Zwischenstände
|-- ic_01.png               # Beispielbild oder Testbild
|
|-- image/
     |-- [dynamisch generierte Tagesordner]
          |-- 01_[format]/        # Sortierte Eingangsdateien
          |-- 02_[outputformat]/  # Konvertierte Ausgabedateien
          |-- 03-Enhancement/     # Vorbereitung für Enhancement
          |-- 03-TransBack/       # Vorbereitung für Transparenz
          |-- ...                 # Weitere Verarbeitungsordner
```

---

Erklärungen (Zusammenfassung)

moduls/ → Basisfunktionen (Logger, Verzeichnisse, Utilities)

settings/ → Steuerdateien für Konfiguration

spelling/ → Alle spezifischen Verarbeitungsskripte

image/ → Arbeitsverzeichnis für Bilder (input/output)

startskript.py → Orchestriert den gesamten Ablauf

log.txt / error_log.txt → Alle Protokollausgaben gesammelt



---

---

```plaintext

START
 |
 v
----------------------------------------
 PHASE 1: INITIALISIERUNG
----------------------------------------
 |
 v
[Startskript.py] -- Startet Ablauf
 |
 v
[Logger] -- Initialisiert Log-Ausgabe
 |
 v
[Utils] -- Bestimmt Arbeitsverzeichnis
 |
 v
[Folders] -- Erstellt Basisordnerstruktur
 |
 v
----------------------------------------
 PHASE 2: DATENVORBEREITUNG
----------------------------------------
 |
 v
[PrepareInput.py] -- Scannt und sortiert Bilder nach Formaten (01_[format])
 |
 v
[Converter.py] -- Konvertiert Bilder ins Ziel-Format (02_[outputformat])
             -- Verteilt kopierte Dateien in 03-Ordner
 |
 v
----------------------------------------
 PHASE 3: SPELLING-STEUERUNG
----------------------------------------
 |
 v
[Spelling.py] -- Lädt spelling.json
 |
 v
--> Für jede Aktivierte Bearbeitungsstufe:
     |
     +--> [Enhancement.py] -- Bildverbesserung
     |
     +--> [TransBack.py] -- Hintergrund entfernen
     |
     +--> [Extract.py] -- Extrahieren
     |
     +--> [ExtractGray.py] -- Graustufenextraktion
     |
     +--> [SwapColors.py] -- Farben tauschen
     |
     +--> [CleanUp.py] -- Aufräumen
     |
     +--> [Scal.py] -- Skalierung
     |
     +--> [Collation.py] -- Zusammenführen
     |
     +--> [invert.py] -- Farben invertieren
 |
 v
END
```
---

Kurz-Erklärung:

Jeder Block [...] = ein Modul

Jeder --> Pfeil = Verzweigung bei aktiver Spelling-Konfiguration

Phasen sind sauber getrennt durch Linien ----------------------------------------

Der Ablauf bleibt linear, außer bei Spelling (hier Mehrfachausführung je Ordner/Skript)


---


---

Modulübersicht


---

Phasen im Detail

Phase 1: Initialisierung

Start über startskript.py

Aktivieren des Loggers (logger.py)

Bestimmen des Arbeitsverzeichnisses (utils.py)

Erstellen der Basisordnerstruktur (folders.py)


Phase 2: Datenvorbereitung

Scannen der Eingabebilder (PrepareInput.py)

Sortieren nach Bildformaten (01_png, 01_webp, etc.)

Konvertieren der Bilder ins Zielformat (z.B. .png) (Converter.py)

Verteilen der konvertierten Bilder auf die Arbeitsordner (03-Enhancement, 03-TransBack, ...)


Phase 3: Spelling-Steuerung

Laden der Konfigurationsdatei spelling.json

Steuern der aktivierten Nachbearbeitungs-Skripte:

Nur Skripte mit "enabled": true werden ausgeführt

Verarbeitung erfolgt Ordnerweise gemäß Konfiguration




---

```plaintext
Beispiel-Konfiguration: spelling.json

{
  "spelling": [
    {
      "name": "Enhancement",
      "enabled": true,
      "folders": ["output_foldes_collation2", "output_foldes_collation4"]
    },
    {
      "name": "Extract",
      "enabled": false,
      "folders": []
    },
    ...
  ]
}

```
"enabled": true → Skript wird aktiv ausgeführt

"folders" → gibt an, auf welche Ordner sich das Skript anwenden soll



---

Technische Hinweise

Logger läuft permanent, um alle Aktionen und Fehler zentral aufzuzeichnen.

Utils verwaltet alle Pfadangaben dynamisch, ohne harte Codierung.

Datenverarbeitung ist modularisiert → neue Skripte können einfach integriert werden.

Fehlerhafte Bilder oder fehlende Ordner werden automatisch erkannt und sauber geloggt.

Skalierbarkeit: Neue Bildformate, neue Verarbeitungsschritte oder neue Ordner können einfach ergänzt werden, ohne Grundlogik zu verändern.

Stabilität: Fehler werden nicht unterdrückt, sondern ordnungsgemäß geloggt und führen nicht zum Programmabbruch.



---

Anforderungen

Python 3.8+

Module (können über requirements.txt installiert werden)


pip install -r requirements.txt


---

```plaintext
Projektstruktur (Kurzform)

ImagesExtract2/
├── moduls/
│   ├── folders.py
│   ├── logger.py
│   └── utils.py
├── settings/
│   ├── start.json
│   ├── foldes.json
│   └── spelling.json
├── spelling/
│   ├── PrepareInput.py
│   ├── Converter.py
│   ├── Spelling.py
│   ├── Enhancement.py
│   ├── Extract.py
│   ├── SwapColors.py
│   └── ...
├── startskript.py
└── README.md
```
---

Lizenz

Dieses Projekt steht unter einer freien Lizenz (bitte anpassen je nach gewünschter Lizenz).


---

Hinweise für Entwickler

Strikte Modultrennung beachten.

Nur Logger für Ausgaben verwenden.

Pfad- und Dateiprüfungen in Utils oder jeweiligen Modulen durchführen.

Fehler dürfen niemals unprotokolliert auftreten.



---

Schlussbemerkung

ImagesExtract2 ist konzipiert für:

große Bildmengen

strukturierte Weiterverarbeitung

hohe Modularität und Erweiterbarkeit

maximale Stabilität und Fehlerkontrolle


---

