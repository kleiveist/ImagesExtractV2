import os
import configparser
import sys
import datetime
import json
from PIL import Image
from pathlib import Path

# Pfad zum mdouls-Verzeichnis hinzufügen
script_directory = os.path.dirname(os.path.abspath(__file__))
base_directory = os.path.dirname(script_directory)
modules_directory = os.path.join(base_directory, "mdouls")
sys.path.append(modules_directory)

# Jetzt können die Module importiert werden
try:
    from logger import log_message, log_separator, shorten_path, init_logger, ICON_SUCCESS, ICON_ERROR, ICON_WARN, ICON_DELETE, ICON_ARROW
    from utils import load_start_config
except ImportError as e:
    print(f"Fehler beim Importieren von Modulen: {e}")
    sys.exit(1)

# **1. LOAD SETTINGS.INI**
config_path = os.path.join(script_directory, "settings.ini")
config = configparser.ConfigParser()
config.read(config_path)

output_format = config["Settings"]["output_format"]
if not output_format.startswith("."):
    output_format = "." + output_format
output_format = output_format.lower()

supported_formats = [".webp", ".bmp", ".jpg", ".jpeg", ".png", ".tiff"]

# **2. START.JSON KONFIGURATION LADEN**
start_config = load_start_config()
folder_config = start_config.get("folder", {})

# **3. ENTRANCE PATH AUSLESEN**
entrance_path = folder_config.get("entrancepath")

# **4. CHECK HOW THE SCRIPT WAS STARTED**
if len(sys.argv) > 1:
    # Arbeitsverzeichnis (wohin die Dateien geschrieben werden)
    base_folder = sys.argv[1]
else:
    base_folder = os.getcwd()

# **5. EINGANGSVERZEICHNIS BESTIMMEN**
source_folder = entrance_path if entrance_path else base_folder
source_folder = Path(source_folder)

# Überprüfen, ob das Eingangsverzeichnis existiert
if not source_folder.exists():
    print(f"Fehler: Das Eingangsverzeichnis '{source_folder}' existiert nicht.")
    sys.exit(1)

# **6. CHECK IF FILES EXIST (BEFORE CREATING A FOLDER)**
files_to_convert = [
    file for file in os.listdir(source_folder)
    if os.path.splitext(file)[1].lower() in supported_formats
]

if not files_to_convert:
    print(f"Keine konvertierbaren Dateien im Verzeichnis '{source_folder}' gefunden. Skript wird beendet.")
    sys.exit(0)  # Exit script

# **7. INITIALIZE LOGGER**
init_logger(base_folder)
script_name = os.path.basename(__file__)  # Dynamically get the script's filename
log_message(f"{script_name} gestartet mit Zielordner: {shorten_path(base_folder)}", level="info")
log_message(f"Eingangsverzeichnis: {shorten_path(str(source_folder))}", level="info")

# **8. CREATE NEW DATE-NAMED FOLDER**
today_str = datetime.datetime.now().strftime("%y%m%d")
new_folder = os.path.join(base_folder, today_str)

counter = 1
while os.path.exists(new_folder):
    new_folder = os.path.join(base_folder, f"{today_str}_{counter:02d}")
    counter += 1

os.makedirs(new_folder)
log_message(f"Neuer Arbeitsordner: {shorten_path(new_folder)}", level="info")

# **9. AUTOMATICALLY SORT & MOVE FILES**
log_separator()
log_message("Sortiere Dateien:", level="info")

file_dict = {}

for file in files_to_convert:
    file_ext = os.path.splitext(file)[1].lower()
    target_folder = os.path.join(new_folder, f"01-{file_ext.strip('.')}")
    os.makedirs(target_folder, exist_ok=True)

    original_path = os.path.join(source_folder, file)
    new_path = os.path.join(target_folder, file)

    # Kopieren statt Verschieben, wenn Quelle und Ziel unterschiedlich sind
    if str(source_folder) != base_folder:
        import shutil
        shutil.copy2(original_path, new_path)
        log_message(f"  - {file} {ICON_ARROW} {shorten_path(target_folder)} (kopiert)", level="info")
    else:
        os.rename(original_path, new_path)
        log_message(f"  - {file} {ICON_ARROW} {shorten_path(target_folder)} (verschoben)", level="info")

    if file_ext not in file_dict:
        file_dict[file_ext] = []
    file_dict[file_ext].append(new_path)

# **10. CREATE OUTPUT FOLDER**
output_folder = os.path.join(new_folder, f"02-{output_format.strip('.')}")
os.makedirs(output_folder, exist_ok=True)

# **11. START CONVERSION**
log_separator()
log_message(f"Starte Konvertierung nach {output_format.upper()}", level="info")

for file_ext, files in file_dict.items():
    for file_path in files:
        file_name = os.path.basename(file_path)
        output_file = os.path.splitext(file_name)[0] + output_format
        output_path = os.path.join(output_folder, output_file)

        try:
            with Image.open(file_path) as img:
                img.save(output_path, output_format.strip(".").upper())
            log_message(f"  - {file_name} {ICON_ARROW} {output_file} {ICON_SUCCESS} Erfolgreich ", level="info")
        except Exception as e:
            log_message(f"  - {file_name} {ICON_ERROR} Fehler: {e}", level="error")

log_separator()
log_message(f"Alle konvertierten Dateien wurden gespeichert in\n'{shorten_path(output_folder)}'.", level="info")
