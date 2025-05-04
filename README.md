Gesamt-Ablauflogik ImagesExtract2 (Stand: aktuelle Phase)

---

1. Startskript
Datei: startskript.py

Aufgabe: Initialisiert das gesamte Programm.

Erstell Datumsordner und legt zielort fest.

Startet die Instanzen:
Logger
Utils
Folders
PrepareInput
Converter
Spelling

---

2. Logger
Datei: init/logger.py

Aufgabe:

Initialisiert Logging (Konsole und/oder log.txt / error_log.txt).

Kontrolliert Ausgaben und Fehlerprotokollierung global.

---

3. Utils
Datei: init/utils.py

Aufgabe:

Legt das Arbeitsverzeichnis fest:

Entweder aus start.json

Oder Standardpfad /images/ im Projekt.

Bietet Zugriffsfunktionen für alle anderen Module auf Pfadinformationen.

Lädt alle Einstellungen aus JSON-Dateien
---

4. Folders
Datei: modules/folders.py

Aufgabe:

Erstellt die Basisordnerstruktur aus settings/foldes.json.

Verwaltung und Prüfung auf Existenz / Neuanlage.

---

5. PrepareInput
Datei: spelling/PrepareInput.py

Aufgabe:

Scannt Eingangsordner.

Ermittelt Bildformate (.png, .jpg, .webp, usw.).

Erstellt dynamische Ordner:

01_png/, 01_webp/, etc.

Verschiebt/kopiert Bilder in die entsprechenden 01-Ordner.

---

6. Converter
Datei: spelling/Converter.py

Aufgabe:

Konvertiert Bilder aus 01_[format]/ in ein definiertes Zielformat (.png).

Speichert konvertierte Bilder in:

neuen Ordner 02_[outputformat] (z.B. 02_png/)

Kopiert die Bilder zusätzlich in alle Ordner, die folders.py angelegt hat (z.B. 03-Enhancement/, 03-TransBack/, usw.).

---

7. Spelling-Steuerung
Datei: spelling/Spelling.py

Aufgabe:

Liest Konfiguration aus settings/spelling.json.

Steuert, welche Nachbearbeitungs-Skripte auf welchen Ordnern ausgeführt werden.

Führt nur enabled: true Skripte aus.

Beispiele: Enhancement, Extract, SwapColors, CleanUp usw.



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

📂 ImagesExtract2
├── 📝 .gitignore
├── 📝 InContent.txt
├── 📝 README.md
├── 📂 entrance/
├── 📝 error_log.txt
├── 📄 ic_01.png
├── 📂 image/
├── 📂 init/
│   ├── 🐍 folders.py
│   ├── 🐍 logger.py
│   └── 🐍 utils.py
├── 📝 log.txt
├── 📂 moduls/
│   ├── 🐍 convert.py
│   └── 🐍 prepareInput.py
├── 📂 settings/
│   ├── 📂 _archive/
│   │   └── 📄 settings.ini
│   ├── 📄 foldes.json
│   ├── 📄 settings.json
│   ├── 📄 spelling.json
│   └── 📄 start.json
├── 📂 spelling/
│   ├── 🐍 CleanUp.py
│   ├── 🐍 Collation.py
│   ├── 🐍 Enhancement.py
│   ├── 🐍 Extract.py
│   ├── 🐍 ExtractGray.py
│   ├── 🐍 Scal.py
│   ├── 🐍 SwapColors.py
│   ├── 🐍 TransBack.py
│   └── 🐍 invert.py
└── 🐍 startskript.py
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
---
Ordner­erstellungs­logik in der start.json
```plaintext
  "folder": {
    "foldername": "image",
    "folderpath": null,
→ Ein Datums­ordner wird im Projekt­verzeichnis unter image angelegt.
```
---
```plaintext
  "folder": {
    "foldername": null,
    "folderpath": null,
→ Ein Datums­ordner wird im aktuellen Arbeits­verzeichnis erstellt.
```
---
```plaintext
  "folder": {
    "foldername": "image",
    "folderpath": "X:\\Blobbite",
→ Ein Datums­ordner wird in X:\Blobbite\image angelegt.
```
---
```plaintext
  "folder": {
    "foldername": null,
    "folderpath": "X:\\Blobbite",
→ Ein Datums­ordner wird direkt in X:\Blobbite erstellt.
```
---
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

