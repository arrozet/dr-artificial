import json
import os
from pathlib import Path

        
        
# Funciones para manejar los chats de los usuarios, cuando haya más de uno 

def load_json(id_usuario):
    #Carga el contenido del archivo JSON.
    json_file = Path(__file__).resolve().parent.parent.parent / "datos" / "chats" / f"chat_{id_usuario}.json"
    with json_file.open("r", encoding="utf-8") as file:  # Ahora `open()` es válido
        return json.load(file)
    
def save_json(data, id_usuario):
    #Guarda los datos en el archivo JSON.
    json_file = Path(__file__).resolve().parent.parent.parent / "datos" / "chats" / f"chat_{id_usuario}.json"
    with json_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)