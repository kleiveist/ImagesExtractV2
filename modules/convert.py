#!/usr/bin/env python3
import os
import sys
import datetime
import json
from PIL import Image
from pathlib import Path

# Pfad zum modules-Verzeichnis hinzufügen
script_directory = os.path.dirname(os.path.abspath(__file__))
base_directory = os.path.dirname(script_directory)
modules_directory = os.path.join(base_directory, "modules")
init_directory = os.path.join(base_directory, "init")  # DIESE ZEILE HINZUFÜGEN
sys.path.append(modules_directory)
sys.path.append(init_directory)  # DIESE ZEILE HINZUFÜGEN

# Module importieren
try:
    from logger import log_message, log_separator, shorten_path, init_logger
    from utils import load_start_config, get_output_format, get_folders_mapping
except ImportError as e:
    print(f"Fehler beim Importieren von Modulen: {e}")
    sys.exit(1)

# Prüfe, wie das Skript gestartet wurde
if len(sys.argv) > 1:
    # Arbeitsverzeichnis (wohin die Dateien geschrieben werden)
    base_folder = sys.argv[1]
else:
    base_folder = os.getcwd()

# Logger initialisieren
init_logger(base_folder)
script_name = os.path.basename(__file__)
log_message(f"{script_name} gestartet mit Zielordner: {shorten_path(base_folder)}", level="info")

# START.JSON Konfiguration laden
start_config = load_start_config()
folder_config = start_config.get("folder", {})

# EINGANGSVERZEICHNIS BESTIMMEN
entrance_path = folder_config.get("entrancepath")
source_folder = entrance_path if entrance_path else base_folder
source_folder = Path(source_folder)

# Ausgabeformat ermitteln
output_format = get_output_format()
if not output_format.startswith("."):
    output_format = "." + output_format
output_format = output_format.lower()

# Überprüfen, ob das Eingangsverzeichnis existiert
if not source_folder.exists():
    log_message(f"Fehler: Das Eingangsverzeichnis '{source_folder}' existiert nicht.", level="error")
    sys.exit(1)

# Datei mit unterstützen Formaten
supported_formats = [".webp", ".bmp", ".jpg", ".jpeg", ".png", ".tiff"]

# Nach konvertierbaren Dateien suchen
files_to_convert = [
    file for file in os.listdir(source_folder)
    if os.path.splitext(file)[1].lower() in supported_formats
]

if not files_to_convert:
    log_message(f"Keine konvertierbaren Dateien im Verzeichnis '{source_folder}' gefunden. Skript wird beendet.", level="info")
    sys.exit(0)

# Ordnerstruktur erstellen
log_separator()
log_message("Sortiere Dateien:", level="info")

file_dict = {}

for file in files_to_convert:
    file_ext = os.path.splitext(file)[1].lower()
    target_folder = os.path.join(base_folder, f"01-{file_ext.strip('.')}")
    os.makedirs(target_folder, exist_ok=True)

    original_path = os.path.join(source_folder, file)
    new_path = os.path.join(target_folder, file)

    # Kopieren statt Verschieben, wenn Quelle und Ziel unterschiedlich sind
    if str(source_folder) != base_folder:
        import shutil
        shutil.copy2(original_path, new_path)
        log_message(f"  - {file} -> {shorten_path(target_folder)} (kopiert)", level="info")
    else:
        os.rename(original_path, new_path)
        log_message(f"  - {file} -> {shorten_path(target_folder)} (verschoben)", level="info")

    if file_ext not in file_dict:
        file_dict[file_ext] = []
    file_dict[file_ext].append(new_path)

# Ausgabeordner erstellen
output_folder = os.path.join(base_folder, f"02-{output_format.strip('.')}")
os.makedirs(output_folder, exist_ok=True)

# Konvertierung starten
log_separator()
log_message(f"Starte Konvertierung nach {output_format.upper()}", level="info")

# Ordnerzuordnungen holen
folders_mapping = get_folders_mapping()

for file_ext, files in file_dict.items():
    for file_path in files:
        file_name = os.path.basename(file_path)
        output_file = os.path.splitext(file_name)[0] + output_format
        output_path = os.path.join(output_folder, output_file)

        try:
            # Bild konvertieren
            with Image.open(file_path) as img:
                img.save(output_path, output_format.strip(".").upper())
            log_message(f"  - {file_name} -> {output_file} erfolgreich konvertiert", level="info")
            
            # Bild in alle 03-Ordner kopieren
            for folder_key, folder_name in folders_mapping.items():
                target_folder = os.path.join(base_folder, f"03-{folder_name}")
                if os.path.exists(target_folder):
                    target_path = os.path.join(target_folder, output_file)
                    import shutil
                    shutil.copy2(output_path, target_path)
                    log_message(f"  - {output_file} -> {shorten_path(target_folder)} kopiert", level="info")
                
        except Exception as e:
            log_message(f"  - {file_name} Fehler: {e}", level="error")

log_separator()
log_message(f"Alle konvertierten Dateien wurden gespeichert in\n'{shorten_path(output_folder)}'.", level="info")
log_message("Bilder wurden in alle 03-Ordner kopiert", level="info")
