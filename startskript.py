#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Basispfad des Projekts ermitteln
base_directory = Path(__file__).parent.absolute()

# Pfade zu den wichtigen Verzeichnissen
modules_directory = base_directory / "modules"
init_directory = base_directory / "init"      # init-Verzeichnis hinzufügen!
settings_directory = base_directory / "settings"
spelling_directory = base_directory / "spelling"
start_config_path = settings_directory / "start.json"

# Alle Verzeichnisse zum Importpfad hinzufügen
sys.path.append(str(modules_directory))
sys.path.append(str(init_directory))          # Dies ist der wichtige Teil!
sys.path.append(str(spelling_directory))

# Logger importieren (aus init/ Verzeichnis)
try:
    from init.logger import log_message, log_separator, init_logger
except ImportError:
    print("Fehler: logger.py konnte nicht importiert werden.")
    sys.exit(1)

# Initialisiere den Logger
init_logger(str(base_directory))

log_separator()
log_message(f"Starte Skript im Verzeichnis: {base_directory}", level="info")

# Einstellungen aus start.json laden
if not start_config_path.exists():
    log_message(f"Konfigurationsdatei nicht gefunden: {start_config_path}", level="error")
    sys.exit(1)

try:
    with open(start_config_path, 'r', encoding='utf-8') as f:
        start_config = json.load(f)
except Exception as e:
    log_message(f"Fehler beim Laden der Konfiguration: {e}", level="error")
    sys.exit(1)

# Ordnerkonfiguration verarbeiten
folder_config = start_config.get("folder", {})
folder_name = folder_config.get("foldername", "image")
folder_path = folder_config.get("folderpath")
entrance_path = folder_config.get("entrancepath")

# Eingangsverzeichnis anzeigen wenn gesetzt
if entrance_path:
    log_message(f"Eingangsverzeichnis (entrancepath): {entrance_path}", level="info")
else:
    log_message("Kein spezielles Eingangsverzeichnis definiert. Verwende Arbeitsverzeichnis.", level="info")

# Erstelle den Zielordner basierend auf der Konfiguration
work_directory = base_directory

# Aktuelles Datum im Format JJMMTT
current_date = datetime.now().strftime("%y%m%d")

# Hier beginnt die Fix: korrekter Umgang mit null/None-Werten
if folder_name is None or folder_name == "null":
    # Wenn foldername null ist, verwenden wir das Basisverzeichnis direkt
    main_folder_path = work_directory
    log_message(f"Verwende Basisverzeichnis direkt: {main_folder_path}", level="info")
else:
    # Sonst erstellen wir den definierten Unterordner
    main_folder_path = work_directory / folder_name
    if not main_folder_path.exists():
        try:
            main_folder_path.mkdir(parents=True)
            log_message(f"Hauptordner erstellt: {main_folder_path}", level="info")
        except Exception as e:
            log_message(f"Fehler beim Erstellen des Hauptordners: {e}", level="error")
            sys.exit(1)

# Bestimme, ob bereits Datumsordner existieren
existing_folders = []
try:
    for folder in os.listdir(main_folder_path):
        folder_path_obj = main_folder_path / folder
        if folder_path_obj.is_dir() and folder.startswith(current_date):
            existing_folders.append(folder)
except Exception as e:
    log_message(f"Fehler beim Auflisten der Ordner: {e}", level="error")

# Bestimme den neuen Ordnernamen
if not existing_folders:
    new_folder_name = current_date
else:
    # Finde die höchste Nummer und erhöhe sie um 1
    max_suffix = 0
    for folder in existing_folders:
        if "_" in folder:
            try:
                suffix = int(folder.split("_")[1])
                max_suffix = max(max_suffix, suffix)
            except (ValueError, IndexError):
                pass
    new_folder_name = f"{current_date}_{max_suffix+1:02d}"

# Erstelle den datumsspezifischen Unterordner
date_folder_path = main_folder_path / new_folder_name
try:
    date_folder_path.mkdir(parents=True, exist_ok=True)
    log_message(f"Datumsordner erstellt: {date_folder_path}", level="info")
except Exception as e:
    log_message(f"Fehler beim Erstellen des Datumsordners: {e}", level="error")
    sys.exit(1)

# Variable für Zielordner initialisieren
target_folder_path = None

# Wenn ein externer Pfad angegeben ist
if folder_path and folder_path.lower() != "none":
    try:
        # Erstelle den Zielpfad falls nicht vorhanden
        target_path = Path(folder_path)
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)

        if folder_name is None or folder_name == "null":
            # Wenn foldername null ist, verwende den Zielpfad direkt
            target_folder_path = target_path
            # Erstelle den Datumsordner direkt im Zielpfad
            external_date_folder = target_folder_path / new_folder_name
            
            # Erstelle den Datumsordner im externen Pfad
            if not external_date_folder.exists():
                external_date_folder.mkdir(parents=True, exist_ok=True)
                
            # Aktualisiere date_folder_path für spätere Verwendung
            date_folder_path = external_date_folder
            log_message(f"Datumsordner direkt im externen Pfad erstellt: {date_folder_path}", level="info")
        else:
            # Erstelle den benannten Unterordner im Zielpfad
            target_folder_path = target_path / folder_name
            
            # Wenn der Ordner bereits am Ziel existiert, lösche ihn
            if target_folder_path.exists():
                shutil.rmtree(target_folder_path)

            # Verschiebe den Hauptordner in den Zielpfad
            shutil.move(str(main_folder_path), str(target_path))
            log_message(f"Ordner verschoben nach: {target_folder_path}", level="info")
            
            # Aktualisiere date_folder_path für spätere Verwendung
            date_folder_path = target_folder_path / new_folder_name

        # Arbeitsverzeichnis aktualisieren
        work_directory = target_path
    except Exception as e:
        log_message(f"Fehler beim Verarbeiten des externen Pfades: {e}", level="error")
        # Falls ein Fehler auftritt, behalten wir den lokalen Pfad bei

# Liste der auszuführenden Skripte vorbereiten
scripts_to_run = []
for module in start_config.get("modules", []):
    module_name = module.get("name")
    module_enabled = module.get("enabled", False)

    if not module_name or not module_enabled:
        continue

    # Hier berücksichtigen wir sowohl Groß- als auch Kleinschreibung
    # und suchen in allen relevanten Verzeichnissen
    search_paths = []

    # Prüfe alle Kombinationen aus Verzeichnis und Dateiendung
    for directory in [modules_directory, init_directory, base_directory, settings_directory, spelling_directory]:
        # Prüfe die exakte Schreibweise
        search_paths.append(directory / f"{module_name}.py")
        # Prüfe die Kleinschreibung
        search_paths.append(directory / f"{module_name.lower()}.py")

    module_path = None
    for path in search_paths:
        if path.exists():
            module_path = path
            log_message(f"Modul {module_name} gefunden unter: {module_path}", level="info")
            break

    if module_path:
        scripts_to_run.append((module_name, str(module_path)))
    else:
        search_locations = "modules, init, Hauptverzeichnis, settings und spelling"
        log_message(f"Modul {module_name} nicht gefunden. Gesucht in: {search_locations}", level="warning")
        log_message(f"Suchpfade geprüft: {[str(p) for p in search_paths]}", level="info")

# Skripte ausführen
for script_name, script_path in scripts_to_run:
    log_message(f"Starte Modul: {script_name}", level="info")

    try:
        # Starte das Skript mit dem aktuellen Verzeichnis als Argument
        subprocess.run(["python", script_path, str(date_folder_path)], check=True)
        log_message(f"Modul {script_name} erfolgreich beendet", level="info")
    except subprocess.CalledProcessError as e:
        log_message(f"Fehler bei der Ausführung von {script_name}: {e}", level="error")
        sys.exit(1)

log_separator()

# Prüfen, ob Bestätigung per Enter-Taste erforderlich ist
enter_confirmation = start_config.get("settings", {}).get("enter_confirmation", False)
if enter_confirmation:
    input("Drücken Sie die Enter-Taste, um das Programm zu beenden...")