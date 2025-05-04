import logging
import os
import json
import textwrap
from datetime import datetime

# Globaler Fehler-Logger und Lazy-Initialization für Logging
_error_logger = None
logging_initialized = False

def load_logger_config():
    """
    Lädt die Logger-Konfiguration aus start.json.
    Gibt Standard-Werte zurück, falls die Datei nicht existiert oder keine Logger-Einstellungen enthält.
    """
    # Standard-Einstellungen
    config = {
        "logger_folder": False,
        "logging_enabled": True,
        "console_output": True
    }
    
    # Versuche, die Konfiguration aus start.json zu laden
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(script_dir)  # Übergeordnetes Verzeichnis von mdouls
        config_path = os.path.join(base_dir, "settings", "start.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                json_config = json.load(f)
                if "logger" in json_config:
                    for key in config:
                        if key in json_config["logger"]:
                            config[key] = json_config["logger"][key]
    except Exception as e:
        print(f"[WARN] Fehler beim Laden der Logger-Konfiguration: {e}")
    
    return config

# Logger-Konfiguration laden
logger_config = load_logger_config()
logger_folder = logger_config["logger_folder"]
logging_enabled = logger_config["logging_enabled"]
console_output = logger_config["console_output"]

def initialize_logging():
    """Initialisiert die Logging-Konfiguration (lazy)."""
    global logging_initialized
    if not logging_initialized:
        base_logger_dir = os.getcwd()  # Basisordner: Arbeitsverzeichnis
        if logger_folder:
            # Erstelle den Ordner _log falls er nicht existiert
            log_dir = os.path.join(base_logger_dir, "_log")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            log_file_path = os.path.join(log_dir, "log.txt")
        else:
            log_file_path = os.path.join(base_logger_dir, "log.txt")
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
            encoding="utf-8"
        )
        logging_initialized = True

def get_error_logger():
    """
    Initialisiert und liefert einen Error-Logger, der für Warnungen, Errors und Deletes genutzt wird.
    Dieser Logger schreibt in error_log.txt.
    """
    global _error_logger
    if _error_logger is None:
        base_logger_dir = os.getcwd()
        if logger_folder:
            log_dir = os.path.join(base_logger_dir, "_log")
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            error_log_path = os.path.join(log_dir, "error_log.txt")
        else:
            error_log_path = os.path.join(base_logger_dir, "error_log.txt")
        _error_logger = logging.getLogger("error_logger")
        _error_logger.propagate = False
        _error_logger.setLevel(logging.INFO)
        handler = logging.FileHandler(error_log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        _error_logger.addHandler(handler)
    return _error_logger

# **ASCII-Symbole für Log-Level**
ICON_SUCCESS = "[OK]"
ICON_ERROR   = "[ERROR]"
ICON_WARN    = "[WARN]"
ICON_INFO    = "[INFO]"
ICON_DELETE  = "[DELETE]"
ICON_ARROW   = "->"

# **Basisverzeichnis für relative Pfade**
BASE_DIRECTORY = None

def init_logger(base_directory):
    """Initialisiert das Logging und speichert das Basisverzeichnis für verkürzte Pfade."""
    global BASE_DIRECTORY
    BASE_DIRECTORY = base_directory

    # Sicherstellen, dass die Logging-Konfiguration initialisiert wird
    if logging_enabled:
        if not logging_initialized:
            initialize_logging()
        log_separator()
        log_message("Working directory:", level="info")
        log_message(BASE_DIRECTORY, level="info")
        log_separator()
    # Unabhängig von logging_enabled: Error-Logger initialisieren,
    # damit error_log.txt immer erstellt wird
    get_error_logger()

def shorten_path(path, max_length=45):
    """
    Verkürzt lange Dateipfade mit "..." und zeigt sie relativ zu BASE_DIRECTORY an.
    """
    if BASE_DIRECTORY and str(path).startswith(str(BASE_DIRECTORY)):
        relative_path = os.path.relpath(str(path), str(BASE_DIRECTORY))
        result = os.path.join("...", relative_path)
    else:
        result = str(path)

    if len(result) > max_length:
        part_length = (max_length - 3) // 2
        result = f"{result[:part_length]}...{result[-part_length:]}"
    return result

def shorten_path_last_n(path, n=4):
    """Verkürzt den Pfad, sodass nur die letzten n Verzeichnisse + Dateiname angezeigt werden."""
    path_parts = str(path).split(os.sep)
    if len(path_parts) > n:
        return os.path.join("...", *path_parts[-n:])
    return str(path)  # Ist der Pfad kurz genug, unverändert zurückgeben

def format_log_message(message):
    """Formatiert lange Log-Nachrichten (max. 90 Zeichen pro Zeile)."""
    return "\n".join(textwrap.wrap(str(message), width=90))

def log_message(message, level=None):
    """
    Schreibt eine Nachricht in den Hauptlog (z. B. log.txt).
    Wird ein Log-Level angegeben, erscheint ein entsprechendes Symbol vorangestellt.
    Zusätzlich werden Meldungen der Typen "warning", "error" und "delete"
    an den Error-Logger weitergeleitet (und somit in error_log.txt geschrieben).
    """
    if logging_enabled and not logging_initialized:
        initialize_logging()

    formatted_message = format_log_message(message)

    # Zuordnung der Icons zu den Log-Levels:
    log_levels = {
        "info": ICON_INFO,
        "warning": ICON_WARN,
        "error": ICON_ERROR,
        "delete": ICON_DELETE
    }

    if level is None:
        log_entry = formatted_message
    else:
        log_entry = f"{log_levels.get(level, ICON_INFO)} {formatted_message}"

    # Schreibe in den Hauptlog (z. B. log.txt), sofern aktiviert.
    if logging_enabled:
        logging.info(log_entry)

    # Bei Warnungen, Errors und Deletes immer in den Error-Logger schreiben und ausgeben:
    if level in ["warning", "error", "delete"]:
        get_error_logger().info(log_entry)
        print(log_entry)
    # Bei Info-Meldungen (oder ohne Level) abhängig vom console_output:
    elif console_output:
        print(log_entry)

def log_separator():
    """Fügt eine Trennlinie in den Log (und ggf. in der Konsole) ein."""
    log_message("-" * 66, level="info")

def log_sub_separator():
    """Fügt eine Untertrennlinie in den Log ein (z. B. zur Gruppierung von Dateioperationen)."""
    log_message("- " * 33, level="info")