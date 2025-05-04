#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

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
modules_dir = os.path.join(base_dir, "mdouls")
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
        ICON_INFO,
        ICON_ARROW
    )
    from utils import (
        load_start_config,
        load_json_config,
        get_output_format,
        find_latest_date_folder,
        supported_extensions
    )
except ImportError as e:
    print(f"Fehler beim Importieren von Modulen: {e}")
    sys.exit(1)

# Logger initialisieren
init_logger(working_dir)

# Ausgabeformat und Ordnerzuordnungen laden
start_config = load_start_config()
output_format = get_output_format()
folder_config = start_config.get("folder", {})

def find_images_in_directory(directory):
    """
    Durchsucht das angegebene Verzeichnis nach Bilddateien und gibt eine Liste von Dateipfaden zurück.
    """
    image_files = []
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                file_ext = os.path.splitext(file)[1].lower().lstrip('.')
                if file_ext in supported_extensions:
                    image_files.append(os.path.join(root, file))
    except Exception as e:
        log_message(f"Fehler beim Durchsuchen des Verzeichnisses {directory}: {e}", level="error")
    
    log_message(f"{len(image_files)} Bilddateien gefunden.", level="info")
    return image_files

def sort_images_by_format(image_files, date_folder):
    """
    Sortiert die gefundenen Bilddateien nach ihrem Format und kopiert sie in entsprechende Unterordner.
    """
    format_count = {}  # Zählt, wie viele Dateien pro Format verarbeitet wurden
    
    for file_path in image_files:
        try:
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')
            
            # Erstelle einen Unterordner für dieses Format
            format_folder = os.path.join(date_folder, f"01-{file_ext}")
            os.makedirs(format_folder, exist_ok=True)
            
            # Zielort für die Datei
            target_path = os.path.join(format_folder, file_name)
            
            # Prüfe, ob die Zieldatei bereits existiert
            if os.path.exists(target_path):
                log_message(f"Datei existiert bereits: {shorten_path(target_path)}", level="warning")
                # Optional: Füge einen Zähler hinzu, um Duplikate zu vermeiden
                counter = 1
                base_name, ext = os.path.splitext(file_name)
                while os.path.exists(target_path):
                    new_name = f"{base_name}_{counter}{ext}"
                    target_path = os.path.join(format_folder, new_name)
                    counter += 1
                log_message(f"Verwende alternativen Namen: {os.path.basename(target_path)}", level="info")
            
            # Kopiere die Datei
            shutil.copy2(file_path, target_path)
            log_message(f"{file_name} {ICON_ARROW} {shorten_path(format_folder)}", level="info")
            
            # Zähle die verarbeitete Datei
            format_count[file_ext] = format_count.get(file_ext, 0) + 1
            
        except Exception as e:
            log_message(f"Fehler beim Verarbeiten von {shorten_path(file_path)}: {e}", level="error")
    
    # Ausgabe der Statistik
    log_separator()
    log_message("Übersicht der verarbeiteten Dateien:", level="info")
    for fmt, count in format_count.items():
        log_message(f"  - Format .{fmt}: {count} Dateien", level="info")
    
    return format_count

def prepare_input():
    """
    Hauptfunktion: Scannt Eingangsordner nach Bildern und sortiert sie nach Formaten.
    """
    log_separator()
    log_message("Starte Vorbereitung der Eingabebilder", level="info")
    
    # Bestimme das Arbeitsverzeichnis
    base_dir = os.getcwd()
    
    # Finde den aktuellen Datumsordner
    latest_date_folder = find_latest_date_folder(base_dir)
    
    if not latest_date_folder:
        log_message("Kein gültiger Datumsordner gefunden. Beende PrepareInput.", level="error")
        return
    
    log_message(f"Arbeite im Datumsordner: {shorten_path(latest_date_folder)}", level="info")
    
    # 1. Bestimme den Eingabeordner (entweder aus Konfiguration oder als Parameter)
    input_folder = folder_config.get("inputpath", base_dir)
    if input_folder.lower() == "none":
        input_folder = base_dir
    
    log_message(f"Suche Bilder in: {shorten_path(input_folder)}", level="info")
    
    # 2. Finde alle Bilddateien im Eingabeordner
    image_files = find_images_in_directory(input_folder)
    
    if not image_files:
        log_message("Keine Bilddateien gefunden. Beende PrepareInput.", level="warning")
        return
    
    # 3. Sortiere die Bilder nach Formaten
    log_sub_separator()
    log_message("Sortiere Bilder nach Formaten:", level="info")
    sort_images_by_format(image_files, latest_date_folder)
    
    log_separator()
    log_message("Vorbereitung der Eingabebilder abgeschlossen", level="info")

if __name__ == "__main__":
    prepare_input()