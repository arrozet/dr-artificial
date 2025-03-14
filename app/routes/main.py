from flask import Blueprint, render_template, request
import sys
from pathlib import Path

# Calcula la ruta absoluta a la carpeta "raiz"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "utils"))  # Agregar "utils" al path
from chat_handler import *

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
Cuando enviamos un mensaje, el mensaje llega aquí
"""
@main_bp.route('/', methods=['GET','POST'])
def procesarPeticiones():
    
    data = request.get_json()
    
    prompt = data.get('prompt',None)
    new_chat_name = data.get("new_chat_name",None)
    mensajes_chat = []
    
    if prompt != "" and prompt:
        prompt = data.get('prompt') 
        
        chat_id = data.get("chat_id",datos_guardados["chat_id"])             
        add_message(chat_id=chat_id, text=prompt, sender="usuario")
        add_message(chat_id=chat_id, text="OK", sender="IA") # METER IA
        
    elif new_chat_name != "" and new_chat_name:
        
        chat_id = create_chat(chat_name=new_chat_name)
        datos_guardados["chat_id"] = chat_id;
    else :
        
        chat_id = data.get("chat_id")
        datos_guardados["chat_id"] = chat_id;

        
    chat_list = list_of_chats()
    mensajes_chat = list_of_messages(chat_id)

    return render_template('index.html', chat_list=chat_list,  mensajes_nuevo_chat=mensajes_chat)


""" 
Cuando creamos un nuevo chat, esta función procesa esa petición
"""
@main_bp.route("/new_chat", methods=['POST'])
def new_chat():
    create_chat("Nuevo Chat") # Esto tenemos que cambiarlo    

@main_bp.route('/<chat_name>') #dejar para que no explote
def mostrar_chat(chat_name):
    return render_template(f'{chat_name}.html')

@main_bp.route("/cambiar_chat", methods=['POST'])
def cambiar_chat():
    data = request.get_json()
    chat_id = data.get("chat_id")
    mensajes_nuevo_chat = list_of_messages(chat_id)
    
    return render_template("index.html", mensajes_nuevo_chat=mensajes_nuevo_chat)


