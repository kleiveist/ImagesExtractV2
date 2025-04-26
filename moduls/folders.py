#!/usr/bin/env python3
import os
import sys
import shutil
import re
import json
from datetime import datetime

# Prüfen, ob ein Pfadargument übergeben wurde
if len(sys.argv) > 1:
    # Verwende das übergebene Verzeichnis
    working_dir = sys.argv[1]
else:
    # Ansonsten Standardverzeichnis verwenden
    working_dir = os.getcwd()

# Füge das Modulverzeichnis zum Pfad hinzu
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Übergeordnetes Verzeichnis (Projektverzeichnis)
modules_dir = script_dir  # Wir sind bereits im mdouls-Verzeichnis
sys.path.append(modules_dir)

try:
    from logger import (
        log_message,
        log_separator,
        log_sub_separator,
        shorten_path,
        init_logger,
        ICON_SUCCESS,
        ICON_ERROR,
        ICON_WARN,
        ICON_INFO
    )
    from utils import (
        get_output_format,
        find_latest_date_folder,
        supported_extensions,
        get_folders_mapping,
        get_spelling_config,
        is_module_enabled,
        get_folder_config
    )
except ImportError as e:
    print(f"Fehler beim Importieren von Modulen: {e}")
    sys.exit(1)

# Logger initialisieren
init_logger(working_dir)

# Ausgabeformat und Ordnerzuordnungen laden
output_format = get_output_format()
folders_mapping = get_folders_mapping()

def create_date_folder(target_directory):
    """
    Erstellt einen neuen Datumsordner im Zielverzeichnis, falls keiner existiert.
    Format: JJMMTT oder JJMMTT_XX, wenn ein Ordner mit demselben Datum bereits existiert.
    """
    # Aktuelles Datum im Format JJMMTT
    current_date = datetime.now().strftime("%y%m%d")

    # Prüfe, ob bereits ein Ordner mit diesem Datum existiert
    existing_folders = []
    for folder in os.listdir(target_directory):
        folder_path = os.path.join(target_directory, folder)
        if os.path.isdir(folder_path) and folder.startswith(current_date):
            existing_folders.append(folder)

    # Bestimme den neuen Ordnernamen
    if not existing_folders:
        new_folder_name = current_date
    else:
        # Finde die höchste Nummer und erhöhe sie um 1
        max_suffix = 0
        for folder in existing_folders:
            if "_" in folder:
                suffix = int(folder.split("_")[1])
                max_suffix = max(max_suffix, suffix)
        new_folder_name = f"{current_date}_{max_suffix+1:02d}"

    # Erstelle den neuen Ordner
    new_folder_path = os.path.join(target_directory, new_folder_name)
    try:
        os.makedirs(new_folder_path, exist_ok=True)
        log_message(f"Datumsordner erstellt: {shorten_path(new_folder_path)}", level="info")
    except Exception as e:
        log_message(f"Fehler beim Erstellen des Datumsordners: {e}", level="error")
        return None

    # Erstelle die notwendigen Unterordner (02-format und 03-collation-Ordner)
    output_folder = os.path.join(new_folder_path, f"02-{output_format}")
    try:
        os.makedirs(output_folder, exist_ok=True)
        log_message(f"Ausgabeordner erstellt: {shorten_path(output_folder)}", level="info")
    except Exception as e:
        log_message(f"Fehler beim Erstellen des Ausgabeordners: {e}", level="error")

    # Erstelle alle 03-Ordner basierend auf foldes.json
    for folder_key, folder_name in folders_mapping.items():
        collation_folder_name = f"03-{folder_name}"
        collation_folder_path = os.path.join(new_folder_path, collation_folder_name)
        try:
            os.makedirs(collation_folder_path, exist_ok=True)
            log_message(f"Collation-Ordner erstellt: {shorten_path(collation_folder_path)}", level="info")
        except Exception as e:
            log_message(f"Fehler beim Erstellen des Collation-Ordners: {e}", level="error")

    return new_folder_path

def find_existing_output_folder(parent_folder):
    """
    Sucht im übergebenen Ordner nach dem korrekten `02-[output_format]`-Ordner.
    Falls dieser nicht existiert, wird ein anderer Ordner, der mit "02-" beginnt, zurückgegeben.
    """
    preferred_folder = os.path.join(parent_folder, f"02-{output_format}")

    if os.path.exists(preferred_folder):
        return preferred_folder

    # Falls der bevorzugte Ordner nicht existiert, suche nach irgendeinem Ordner, der mit "02-" anfängt.
    for folder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder)
        if folder.startswith("02-") and os.path.isdir(folder_path):
            log_message(f"Bevorzugter Ordner '{shorten_path(preferred_folder)}' nicht gefunden. Verwende stattdessen '{folder}'.", level="info")
            return folder_path
    return None

def process_folders():
    """
    Hauptfunktion zur Verarbeitung der Ordnerstruktur:
    1. Verwendet den übergebenen Verzeichnispfad (häufig bereits der Datumsordner)
    2. Prüft, ob die erforderlichen Unterordner existieren, falls nicht werden sie erstellt
    """
    log_separator()
    log_message(f"Verarbeite Ordnerstruktur in: {shorten_path(working_dir)}", level="info")

    # Da der Arbeitsordner bereits von startskript.py erstellt wurde,
    # verwenden wir direkt den übergebenen Pfad
    parent_folder = working_dir
    log_message(f"Arbeite im Ordner: {shorten_path(parent_folder)}", level="info")

    # Überprüfe, ob die 02- und 03-Ordner existieren, ansonsten erstelle sie
    output_folder = find_existing_output_folder(parent_folder)
    if not output_folder:
        output_folder = os.path.join(parent_folder, f"02-{output_format}")
        try:
            os.makedirs(output_folder, exist_ok=True)
            log_message(f"Ausgabeordner erstellt: {shorten_path(output_folder)}", level="info")
        except Exception as e:
            log_message(f"Fehler beim Erstellen des Ausgabeordners: {e}", level="error")

    # Erstelle alle 03-Ordner basierend auf foldes.json
    for folder_key, folder_name in folders_mapping.items():
        collation_folder_name = f"03-{folder_name}"
        collation_folder_path = os.path.join(parent_folder, collation_folder_name)
        if not os.path.exists(collation_folder_path):
            try:
                os.makedirs(collation_folder_path, exist_ok=True)
                log_message(f"Collation-Ordner erstellt: {shorten_path(collation_folder_path)}", level="info")
            except Exception as e:
                log_message(f"Fehler beim Erstellen des Collation-Ordners: {e}", level="error")

    log_separator()
    log_message("Ordnerstruktur erfolgreich erstellt/aktualisiert.", level="info")

if __name__ == "__main__":
    process_folders()
