#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

# Pfad zum Modulverzeichnis hinzufügen
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)
modules_dir = os.path.join(base_dir, "modules")  # Korrigiert von "mdouls" zu "modules"
sys.path.append(modules_dir)

try:
    from logger import log_message, log_separator, shorten_path
    from utils import load_json_config, find_latest_date_folder
except ImportError as e:
    print(f"Fehler beim Importieren von Modulen: {e}")
    sys.exit(1)

def run_spelling_script(script_name, target_folder, enabled=True):
    """
    Führt ein Spelling-Skript aus, wenn es aktiviert ist.
    
    :param script_name: Name des auszuführenden Skripts (ohne .py)
    :param target_folder: Zielordner, auf dem das Skript ausgeführt werden soll
    :param enabled: Gibt an, ob das Skript ausgeführt werden soll
    :return: True bei Erfolg, False bei Fehlern
    """
    if not enabled:
        log_message(f"Skript {script_name} ist deaktiviert. Wird übersprungen.", level="info")
        return True
    
    script_path = os.path.join(script_dir, f"{script_name}.py")
    
    if not os.path.exists(script_path):
        log_message(f"Skript {script_name}.py nicht gefunden in {shorten_path(script_dir)}", level="error")
        return False
    
    log_message(f"Führe Skript aus: {script_name}.py auf Ordner {shorten_path(target_folder)}", level="info")
    
    try:
        subprocess.run(["python", script_path, target_folder], check=True)
        log_message(f"Skript {script_name}.py erfolgreich ausgeführt", level="info")
        return True
    except subprocess.CalledProcessError as e:
        log_message(f"Fehler bei der Ausführung von {script_name}.py: {e}", level="error")
        return False

def main():
    # Arbeitsverzeichnis ist entweder das übergebene oder das aktuelle
    if len(sys.argv) > 1:
        working_dir = sys.argv[1]
    else:
        working_dir = os.getcwd()
        
    log_separator()
    log_message(f"Spelling-Verarbeitung wird gestartet in: {shorten_path(working_dir)}", level="info")
    
    # Lade die Konfiguration aus spelling.json
    base_dir = os.path.dirname(script_dir)
    config_path = os.path.join(base_dir, "settings", "spelling.json")
    
    if not os.path.exists(config_path):
        log_message(f"Konfigurationsdatei nicht gefunden: {shorten_path(config_path)}", level="error")
        return
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        log_message(f"Fehler beim Laden der Konfiguration: {e}", level="error")
        return
    
    # Extrahiere die Spelling-Konfiguration
    spelling_config = config.get("spelling", [])
    
    if not spelling_config:
        log_message("Keine Spelling-Konfiguration gefunden. Beende Spelling-Verarbeitung.", level="warning")
        return
    
    # Finde den neuesten Datumsordner
    target_folder = find_latest_date_folder(working_dir) if os.path.isdir(working_dir) else working_dir
    
    # Führe die aktivierten Skripte aus
    for script_config in spelling_config:
        script_name = script_config.get("name")
        enabled = script_config.get("enabled", False)
        folders = script_config.get("folders", [])
        
        if not script_name:
            continue
        
        log_message(f"Verarbeite Skript: {script_name} (aktiviert: {enabled})", level="info")
        
        if enabled:
            run_spelling_script(script_name, target_folder, enabled=True)
    
    log_separator()
    log_message("Spelling-Verarbeitung abgeschlossen", level="info")

if __name__ == "__main__":
    main()