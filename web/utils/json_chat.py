import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "datos" / "chats" / "chats.json"

DATA_USUARIOS_PATH = Path(__file__).resolve().parent.parent.parent / "datos" / "chats" / "chat_"

def load_json():
    """Carga el contenido del archivo JSON."""
    with DATA_PATH.open("r", encoding="utf-8") as file:  # Ahora `open()` es válido
        return json.load(file)

def save_json(data):
    """Guarda los datos en el archivo JSON."""
    with DATA_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
        
        
# Funciones para manejar los chats de los usuarios, cuando haya más de uno 
"""
def load_json(id_usuario):
    #Carga el contenido del archivo JSON.
    json_file =  (DATA_USUARIOS_PATH + id_usuario)
    with json_file.open("r", encoding="utf-8") as file:  # Ahora `open()` es válido
        return json.load(file)
    
def save_json(data, id_usuario):
    #Guarda los datos en el archivo JSON.
    json_file =  (DATA_USUARIOS_PATH + id_usuario)
    with json_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
"""