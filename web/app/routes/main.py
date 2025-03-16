from flask import Blueprint, render_template, request
import os
import sys

# Get project root directory more cleanly
current_dir = os.path.dirname(os.path.abspath(__file__))  # routes folder
app_dir = os.path.dirname(current_dir)                    # app folder
web_dir = os.path.dirname(app_dir)                        # web folder
project_root = os.path.dirname(web_dir)                   # project root

# Add project root to path to enable imports from any module
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import specific functions instead of using wildcard import
from web.utils.chat_handler import (
    list_of_chats,
    list_of_messages,
    add_message,
    create_chat,
    delete_chat
)

main_bp = Blueprint("main", __name__)

datos_guardados = {"chat_id": 0}

""" 
Ruta inicial
Esta ruta es con la que se inicia la página web
"""
@main_bp.route("/")
def home():
    
    chat_id = 1
    # Cargamos todos los chats
    chat_list = list_of_chats()
    
    return render_template("index.html", chat_list=chat_list, mensajes_nuevo_chat=[])


""" 
Cuando recibe una petición POST la página web, esta función resuelve
"""
@main_bp.route('/', methods=['GET','POST'])
def procesarPeticiones():

    data = request.get_json()                       # Cargamos el JSON
    
    chat_id = data.get("chat_id",datos_guardados["chat_id"])             
    prompt = data.get('prompt',None)                
    new_chat_name = data.get("new_chat_name",None)
    borrar_chat_id = data.get("borrar_chat_id", None)
    
    if prompt:                     # Por tanto la petición es de un nuevo mensaje
        prompt = data.get('prompt') 
        
        add_message(chat_id=chat_id, text=prompt, sender="usuario")
        add_message(chat_id=chat_id, text="OK", sender="IA") # METER IA
        
    elif new_chat_name:     # La petición es de crear un nuevo chat
        
        chat_id = create_chat(chat_name=new_chat_name)
        datos_guardados["chat_id"] = chat_id
        
    elif borrar_chat_id:    # La petición es sobre borrar un chat
        delete_chat(borrar_chat_id)
        if chat_id == borrar_chat_id :
            chat_id = 0
        
    else :                                          # La petición es de cargar un chat existente
        
        chat_id = data.get("chat_id")
        datos_guardados["chat_id"] = chat_id


    chat_list = list_of_chats()
    mensajes_chat = list_of_messages(chat_id)

    return render_template('index.html', chat_list=chat_list,  mensajes_nuevo_chat=mensajes_chat)
   

@main_bp.route('/<chat_name>') #dejar para que no explote
def mostrar_chat(chat_name):
    return render_template(f'{chat_name}.html')


