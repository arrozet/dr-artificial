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
Cuando recibe una petición POST la página web, esta función resuelve
"""
@main_bp.route('/', methods=['GET','POST'])
def procesarPeticiones():

    data = request.get_json()                       # Cargamos el JSON
    
    prompt = data.get('prompt',None)                
    new_chat_name = data.get("new_chat_name",None)
    
    if prompt and prompt != "":                     # Por tanto la petición es de un nuevo mensaje
        prompt = data.get('prompt') 
        
        chat_id = data.get("chat_id",datos_guardados["chat_id"])             
        add_message(chat_id=chat_id, text=prompt, sender="usuario")
        add_message(chat_id=chat_id, text="OK", sender="IA") # METER IA
        
    elif new_chat_name and new_chat_name != "":     # La petición es de crear un nuevo chat
        
        chat_id = create_chat(chat_name=new_chat_name)
        datos_guardados["chat_id"] = chat_id;
    else :                                          # La petición es de cargar un chat existente
        
        chat_id = data.get("chat_id")
        datos_guardados["chat_id"] = chat_id;


    chat_list = list_of_chats()
    mensajes_chat = list_of_messages(chat_id)

    return render_template('index.html', chat_list=chat_list,  mensajes_nuevo_chat=mensajes_chat)
   

@main_bp.route('/<chat_name>') #dejar para que no explote
def mostrar_chat(chat_name):
    return render_template(f'{chat_name}.html')


