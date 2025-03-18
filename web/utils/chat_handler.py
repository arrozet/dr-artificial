import json
import os
import sys

# Add current directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Use a relative import with proper path
from .json_chat import *  # Note the dot to indicate relative import

def create_chat(chat_name, id_usuario):
    #Crea un nuevo chat.
    data = load_json(id_usuario)
# Encontrar el ID más alto entre los chats existentes
    max_id = 0
    for chat in data.get("chats", []):
        if chat.get("chat_id", 0) > max_id:
            max_id = chat.get("chat_id")    
    chat_id = max_id + 1  # Incrementar el ID en 1
    new_chat = {
        
        "chat_id": chat_id,
        "chat_name": chat_name,
        "messages": []
    }
    
    data["chats"].append(new_chat)
    save_json(data, id_usuario)
    return chat_id 

def delete_chat(chat_id,id_usuario):
    #Borrar un chat existente.
    data = load_json(id_usuario)  # Cargar los datos desde el JSON
    
    # Filtrar los chats que no coincidan con el nombre dado
    updated_chats = [chat for chat in data.get("chats", []) if chat.get("chat_id") != chat_id]
    
    # Si el número de chats cambió, significa que eliminamos al menos uno
    if len(updated_chats) < len(data.get("chats", [])):
        data["chats"] = updated_chats  # Actualizar la lista de chats
        save_json(data, id_usuario)  # Guardar cambios en el archivo JSON
        return True  # Indicar que se eliminó correctamente
    
    return False  # Indicar que no se encontró el chat

def add_message(chat_id, sender, text, id_usuario):
    #Añade un mensaje a un chat existente.
    data = load_json(id_usuario)  # Cargar el JSON completo
    
    # Buscar el chat por ID
    for chat in data.get("chats", []):
        if str(chat.get("chat_id")) == str(chat_id):  # Convertimos ambos a string para evitar problemas
            chat.setdefault("messages", [])  # Aseguramos que la clave "messages" existe
            
            new_message = {
                "message_id": len(chat["messages"]) + 1,
                "sender": sender,
                "text": text
            }
            chat["messages"].append(new_message)  # Agregar el mensaje
            save_json(data, id_usuario)  # Guardar los cambios en el archivo
            
            return new_message  # Retornar el mensaje agregado
    
    return None  # Si no se encuentra el chat

def list_of_messages(chat_id, id_usuario):
    #Devuelve la lista de mensajes, con el rol de la persona que envió el mensaje, para el chat con el chat_id dado.
    data = load_json(id_usuario)  # Cargar el JSON que contiene todos los chats
    mensajes = []  # Inicializar lista de mensajes
    
    for chat in data.get("chats", []):  # Iterar sobre los chats
        if chat.get("chat_id") == chat_id:
            for message in chat.get("messages", []):
                mensajes.append({
                    "message": message.get("text"),
                    "message_sender": message.get("sender")
                })
            return mensajes  # Devolver todos los mensajes del chat encontrado
    
    return []  # Si no se encuentra el chat_id, devolver una lista vacía

def list_of_chats(id_usuario):
    data = load_json(id_usuario)
    
    chats = []  # Lista para guardar los chats con chat_id y name
    for chat in data.get("chats", []):  # Itera sobre los chats
        chat_info = {
            "chat_id": chat.get("chat_id"),
            "chat_name": chat.get("chat_name")
        }
        chats.append(chat_info)  # Agrega el chat con sus datos
    return chats









