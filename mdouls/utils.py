#!/usr/bin/env python3
import os
import re
import json
import sys
from pathlib import Path

# Prüfen, ob Logger bereits importiert werden kann
try:
    from logger import log_message, shorten_path
except ImportError:
    # Einfache Ersatzfunktionen, falls Logger noch nicht verfügbar
    def log_message(message, level="info"):
        print(f"[{level.upper()}] {message}")

    def shorten_path(path, max_length=45):
        if len(str(path)) > max_length:
            part_length = (max_length - 3) // 2
            return f"{str(path)[:part_length]}...{str(path)[-part_length:]}"
        return str(path)

# ----------------------------------------------------------
# Einstellungen aus JSON-Dateien laden
# ----------------------------------------------------------

def load_start_config():
    """
    Lädt die start.json Konfiguration
    """
    # Bestimme den Pfad zur JSON-Datei
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Übergeordnetes Verzeichnis von mdouls
    config_path = os.path.join(base_dir, "settings", "start.json")

    if not os.path.exists(config_path):
        log_message(f"start.json nicht gefunden: {shorten_path(config_path)}", level="warning")
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        log_message(f"start.json geladen: {shorten_path(config_path)}", level="info")
        return config
    except Exception as e:
        log_message(f"Fehler beim Laden von start.json: {e}", level="error")
        return {}

def load_json_config(file_name):
    """
    Lädt eine JSON-Konfigurationsdatei aus dem Einstellungsverzeichnis.
    Falls die Datei nicht gefunden wird, wird eine Warnung ausgegeben und ein leeres Dict zurückgegeben.
    """
    # Bestimme den Pfad zur JSON-Datei
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Übergeordnetes Verzeichnis von mdouls
    config_path = os.path.join(base_dir, "settings", file_name)

    if not os.path.exists(config_path):
        log_message(f"{file_name} nicht gefunden: {shorten_path(config_path)}", level="warning")
        return {}

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        log_message(f"{file_name} geladen: {shorten_path(config_path)}", level="info")
        return config
    except Exception as e:
        log_message(f"Fehler beim Laden von {file_name}: {e}", level="error")
        return {}

def get_folder_config():
    """
    Lädt die Ordnerkonfiguration aus start.json und gibt sie zurück.
    Gibt ein standardmäßiges Dictionary zurück, wenn keine Konfiguration existiert.
    """
    config = load_start_config()
    folder_config = config.get("folder", {})

    # Standardwerte festlegen, falls nicht vorhanden
    if not "foldername" in folder_config:
        folder_config["foldername"] = "image"
    if not "folderpath" in folder_config:
        folder_config["folderpath"] = None

    log_message(f"Ordner-Konfiguration geladen: {folder_config}", level="info")
    return folder_config
def get_folders_mapping():
    """Lädt die foldes.json-Datei und gibt die Ordnerzuordnung zurück."""
    folders_config = load_json_config("foldes.json")
    return folders_config

def get_spelling_config():
    """Lädt die spelling.json-Datei und gibt die Modulkonfiguration zurück."""
    spelling_config = load_json_config("spelling.json")
    return spelling_config.get("spelling", [])

def get_output_format():
    """
    Ermittelt das Ausgabeformat aus den Einstellungen in start.json.
    Standardmäßig 'png', wenn nichts anderes definiert ist.
    """
    config = load_start_config()
    output_format = config.get("settings", {}).get("output_format", "png")
    log_message(f"Ausgabeformat: {output_format}", level="info")
    return output_format

def is_module_enabled(module_name):
    """
    Prüft, ob ein Modul in start.json aktiviert ist.
    """
    config = load_start_config()
    for module in config.get("modules", []):
        if module.get("name") == module_name:
            return module.get("enabled", False)
    return False

def save_start_config(config):
    """
    Speichert die aktualisierte start.json-Konfiguration
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    config_path = os.path.join(base_dir, "settings", "start.json")

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        log_message(f"start.json aktualisiert: {shorten_path(config_path)}", level="info")
        return True
    except Exception as e:
        log_message(f"Fehler beim Speichern von start.json: {e}", level="error")
        return False

def get_module_folders(module_name):
    """
    Gibt die Liste der Ordner zurück, die für ein bestimmtes Modul in spelling.json konfiguriert sind.
    """
    spelling_config = get_spelling_config()
    for module in spelling_config:
        if module.get("name") == module_name:
            return module.get("folders", [])
    return []

# ----------------------------------------------------------
# Suche nach dem neuesten Datum-Ordner
# ----------------------------------------------------------

def find_latest_date_folder(search_dir):
    """
    Sucht im search_dir nach Ordnern, deren Name dem Muster JJMMTT oder JJMMTT_XX entspricht,
    und liefert den (alphabetisch) letzten zurück.

    Nutzt log_message und shorten_path zur Protokollierung.
    """
    log_message(f"Suche nach Datumsordnern in: {shorten_path(search_dir)}", level="info")

    try:
        entries = os.listdir(search_dir)
    except Exception as e:
        log_message(f"Verzeichnis {search_dir} konnte nicht gelesen werden: {e}", level="error")
        return None

    date_folders = sorted(
        [d for d in entries
         if os.path.isdir(os.path.join(search_dir, d)) and re.match(r"^\d{6}(_\d{2})?$", d)],
        reverse=True
    )

    log_message(f"Gefundene Datumsordner: {date_folders}", level="info")

    if not date_folders:
        log_message("Kein gültiger Datumsordner (JJMMTT oder JJMMTT_XX) gefunden.", level="warning")
        return None

    latest_folder = os.path.join(search_dir, date_folders[0])
    log_message(f"Neuester Datumsordner: {shorten_path(latest_folder)}", level="info")
    return latest_folder

# ----------------------------------------------------------
# Unterstützte Dateiformate
# ----------------------------------------------------------
supported_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']
