import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "datos" / "chats" / "chats.json"

def load_json():
    """Carga el contenido del archivo JSON."""
    with DATA_PATH.open("r", encoding="utf-8") as file:  # Ahora `open()` es válido
        return json.load(file)

def save_json(data):
    """Guarda los datos en el archivo JSON."""
    with DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
