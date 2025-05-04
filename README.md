# ImagesExtract2

## Inhaltsverzeichnis

* [Projektbeschreibung](#projektbeschreibung)
* [Projektstruktur](#projektstruktur)
* [Ablaufübersicht](#ablaufübersicht)
* [Phasen im Detail](#phasen-im-detail)

  * [Phase 1: Initialisierung](#phase-1-initialisierung)
  * [Phase 2: Datenvorbereitung](#phase-2-datenvorbereitung)
  * [Phase 3: Spelling-Steuerung](#phase-3-spelling-steuerung)
* [Modulübersicht](#modulübersicht)
* [Konfiguration](#konfiguration)
* [Installation](#installation)
* [Entwicklerhinweise](#entwicklerhinweise)
* [Lizenz](#lizenz)

---

## Projektbeschreibung

ImagesExtract2 ist ein modulares Bildverarbeitungssystem zur effizienten Verarbeitung und strukturierten Ablage großer Bildmengen. Das System ist in drei Hauptphasen unterteilt und kann durch JSON-basierte Konfiguration flexibel erweitert werden.

## Projektstruktur

```plaintext
ImagesExtract2/
├── .gitignore
├── InContent.txt
├── README.md
├── entrance/
├── error_log.txt
├── ic_01.png
├── image/
├── init/
│   ├── folders.py
│   ├── logger.py
│   └── utils.py
├── log.txt
├── moduls/
│   ├── convert.py
│   └── prepareInput.py
├── settings/
│   ├── _archive/
│   │   └── settings.ini
│   ├── foldes.json
│   ├── settings.json
│   ├── spelling.json
│   └── start.json
├── spelling/
│   ├── CleanUp.py
│   ├── Collation.py
│   ├── Enhancement.py
│   ├── Extract.py
│   ├── ExtractGray.py
│   ├── Scal.py
│   ├── SwapColors.py
│   ├── TransBack.py
│   └── invert.py
└── startskript.py
```

## Ablaufübersicht

```plaintext
START
 |
 v
----------------------------------------
 PHASE 1: INITIALISIERUNG
----------------------------------------
 |
 v
[Startskript.py] -> Logger -> Utils -> Folders
 |
 v
----------------------------------------
 PHASE 2: DATENVORBEREITUNG
----------------------------------------
 |
 v
[PrepareInput.py] -> Converter
 |
 v
----------------------------------------
 PHASE 3: SPELLING-STEUERUNG
----------------------------------------
 |
 v
[Spelling.py] -> aktivierte Skripte (Enhancement, Extract, ...)
 |
 v
END
```

## Phasen im Detail

### Phase 1: Initialisierung

* **startskript.py**: Startpunkt, erstellt Datumsordner, konfiguriert Zielorte und startet alle Module.
* **logger.py**: Initialisiert Logging (Konsole, `log.txt`, `error_log.txt`).
* **utils.py**: Bestimmt Arbeitsverzeichnis, lädt JSON-Einstellungen.
* **folders.py**: Erzeugt Basisordnerstruktur gemäß `settings/foldes.json`.

### Phase 2: Datenvorbereitung

* **PrepareInput.py**: Scannt Eingangsordner, sortiert Bilder in `01_[format]`.
* **Converter.py**: Konvertiert in Ziel­format (`02_[outputformat]`), verteilt in 03-Ordner.

### Phase 3: Spelling-Steuerung

* **Spelling.py**: Liest `settings/spelling.json`, führt nur Skripte mit `enabled: true` aus:

  * Enhancement
  * TransBack
  * Extract
  * ExtractGray
  * SwapColors
  * CleanUp
  * Scal
  * Collation
  * invert

## Modulübersicht

| Modul              | Pfad                       | Aufgabe                                |
| ------------------ | -------------------------- | -------------------------------------- |
| Logger             | `init/logger.py`           | Logging-Initialisierung                |
| Utils              | `init/utils.py`            | Arbeitsverzeichnis, JSON-Einstellungen |
| Folders            | `modules/folders.py`       | Basisordner erstellen                  |
| PrepareInput       | `spelling/PrepareInput.py` | Bilder scannen & sortieren             |
| Converter          | `spelling/Converter.py`    | Bildkonvertierung & Verteilung         |
| Spelling-Steuerung | `spelling/Spelling.py`     | Steuerung der Nachbearbeitungsskripte  |

## Konfiguration

* **settings/start.json**: Einstellungen zu Datumsordnern.
* **settings/foldes.json**: Basisordnerstruktur.
* **settings/spelling.json**: Aktivierte Skripte und Zielordner.

```json
{
  "spelling": [
    {"name": "Enhancement", "enabled": true, "folders": ["03-Enhancement"]},
    {"name": "Extract",     "enabled": false, "folders": []}
  ]
}
```

## Installation

Voraussetzungen: Python 3.8+

```bash
pip install -r requirements.txt
```

## Entwicklerhinweise

* Strikte Trennung der Module.
* Nur `logger.py` für Ausgaben verwenden.
* Pfadprüfungen in `utils.py` bzw. Modulen.
* Fehler werden geloggt, nicht unterdrückt.

## Lizenz

Dieses Projekt steht unter \[Lizenz eintragen].

---

