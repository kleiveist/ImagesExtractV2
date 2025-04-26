from __future__ import annotations

import importlib
import json
import os
import sys
from types import ModuleType
from typing import Any, Dict, List

from _logger import init_logger, log_message, log_separator
from _utils import load_settings_ini, find_latest_date_folder

CONFIG_FILENAME = "modules_config.json"


def _load_module(module_name: str) -> ModuleType | None:
    """Importiert ein Modul dynamisch und gibt es zurück oder ``None`` bei Fehler."""
    try:
        return importlib.import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        log_message(f"[ERROR] Modul '{module_name}' konnte nicht importiert werden: {exc}", level="error")
        return None


def _run_module_on_folder(module: ModuleType, folder: str) -> None:
    """Ruft ``process_folder`` des Moduls für den gegebenen Ordner auf."""
    process_fn = getattr(module, "process_folder", None)
    if not callable(process_fn):
        log_message(
            f"[ERROR] Modul '{module.__name__}' besitzt keine Funktion 'process_folder(folder_path)'.", level="error"
        )
        return

    try:
        process_fn(folder)
        log_message(f"Modul '{module.__name__}' erfolgreich auf '{folder}' angewendet.", level="info")
    except Exception as exc:  # noqa: BLE001
        log_message(f"[ERROR] Fehler in '{module.__name__}' für '{folder}': {exc}", level="error")


def main() -> None:
    base_dir = os.getcwd()
    init_logger(base_dir)

    settings = load_settings_ini()
    latest_date_folder = find_latest_date_folder(base_dir)
    if not latest_date_folder:
        log_message("[FATAL] Kein gültiger Datum‑Ordner gefunden.", level="error")
        sys.exit(1)

    config_path = os.path.join(base_dir, CONFIG_FILENAME)
    if not os.path.isfile(config_path):
        log_message(f"[FATAL] Konfigurationsdatei '{CONFIG_FILENAME}' nicht gefunden.", level="error")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as fh:
        config: Dict[str, Any] = json.load(fh)

    modules_cfg: List[Dict[str, Any]] = config.get("modules", [])
    if not modules_cfg:
        log_message("[FATAL] Keine Module in der Konfiguration gefunden.", level="error")
        sys.exit(1)

    log_separator()
    log_message("Starte Modul‑Verarbeitung …", level="info")

    for mod_cfg in modules_cfg:
        name: str = mod_cfg.get("name", "")
        if not name:
            log_message("[WARN] Ein Eintrag ohne Modulnamen wurde übersprungen.", level="warning")
            continue
        if not mod_cfg.get("enabled", True):
            log_message(f"Modul '{name}' ist deaktiviert – überspringe.", level="info")
            continue

        module = _load_module(name)
        if module is None:
            continue  # Fehler wurde bereits geloggt

        folders_keys: List[str] = mod_cfg.get("folders", [])
        if not folders_keys:
            log_message(f"[WARN] Modul '{name}' hat keine Zielordner definiert.", level="warning")
            continue

        for key in folders_keys:
            folder_setting = settings.get("Settings", key, fallback=None)
            if not folder_setting:
                log_message(f"[WARN] Schlüssel '{key}' nicht in settings.ini gefunden.", level="warning")
                continue
            folder_name = f"03-{folder_setting}"
            target_folder = os.path.join(latest_date_folder, folder_name)
            if not os.path.isdir(target_folder):
                log_message(f"[WARN] Ordner '{target_folder}' existiert nicht.", level="warning")
                continue

            log_message(f"[RUN] {name} -> {target_folder}", level="info")
            _run_module_on_folder(module, target_folder)

    log_separator()
    log_message("Alle aktiven Module wurden ausgeführt.", level="info")


if __name__ == "__main__":  # pragma: no cover
    main()
