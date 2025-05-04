---
---
Ordner­erstellungs­logik in der start.json
```plaintext
  "folder": {
    "foldername": "image",
    "folderpath": null,
→ Ein Datums­ordner wird im Projekt­verzeichnis unter image angelegt.
```
---
```plaintext
  "folder": {
    "foldername": null,
    "folderpath": null,
→ Ein Datums­ordner wird im aktuellen Arbeits­verzeichnis erstellt.
```
---
```plaintext
  "folder": {
    "foldername": "image",
    "folderpath": "X:\\Blobbite",
→ Ein Datums­ordner wird in X:\Blobbite\image angelegt.
```
---
```plaintext
  "folder": {
    "foldername": null,
    "folderpath": "X:\\Blobbite",
→ Ein Datums­ordner wird direkt in X:\Blobbite erstellt.
```
---
---