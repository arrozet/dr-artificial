import json
import os

from json_chat import *;

def create_chat(chat_name):
    """Crea un nuevo chat."""
    data = load_json()
    chat_id = len(data["chats"]) + 1
    new_chat = {
        
        "chat_id": chat_id,
        "chat_name": chat_name,
        "messages": []
    }
    
    data["chats"].append(new_chat)
    save_json(data)
    add_message(chat_id=chat_id, sender="IA", text="¿En qué puedo ayudarte?")
    return chat_id 

def add_message(chat_id, sender, text):
    """Añade un mensaje a un chat existente."""
    data = load_json()  # Cargar el JSON completo
    
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
            save_json(data)  # Guardar los cambios en el archivo
            
            return new_message  # Retornar el mensaje agregado
    
    return None  # Si no se encuentra el chat

def list_of_messages(chat_id):
    """Devuelve la lista de mensajes del chat con el chat_id dado."""
    data = load_json()  # Cargar el JSON que contiene todos los chats
    
    for chat in data.get("chats", []):  # Iterar sobre los chats
        if chat.get("chat_id") == chat_id:
            return chat.get("messages", [])  # Devolver mensajes o lista vacía si no hay
    
    return None  # Si no se encuentra el chat_id

def list_of_chats():
    data = load_json()
    
    chats = []  # Lista para guardar los chats con chat_id y name
    for chat in data.get("chats", []):  # Itera sobre los chats
        chat_info = {
            "chat_id": chat.get("chat_id"),
            "chat_name": chat.get("chat_name")
        }
        chats.append(chat_info)  # Agrega el chat con sus datos
    return chats

print(list_of_chats())