from flask import Blueprint, render_template, request
import sys
from pathlib import Path

# Calcula la ruta absoluta a la carpeta "raiz"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BASE_DIR / "utils"))  # Agregar "utils" al path
from chat_handler import *

main_bp = Blueprint("main", __name__)

#PARA QUE FUNCIONE EN INTERFAZ1 O INDEX CAMBIAR EN DONDE HE COMENTADO
@main_bp.route("/")
def home():
    
    chat_list = list_of_chats()
    
    return render_template("index.html", chat_list=chat_list) # AQUI


@main_bp.route('/', methods=['POST'])
def procesarPrompt():
    prompt = request.form['prompt']  # Elimina espacios en blanco

    mi_mensaje = f"""
        <div class="UserMessage">
            <div class="avatar user">U</div>
            <div class="message-content">
                <div class="message-bubble">
                    {prompt}
                </div>
            </div>
        </div>
        """

    respuesta = "HOLA"
    respuesta_html = f"""
        <div class="AiMessage">
            <div class="avatar">AI</div>
            <div class="message-content">
                <div class="message-bubble">
                    {respuesta}
                </div>
            </div>
        </div>
        """

    if not prompt:  # Validación para evitar enviar texto vacío
        return render_template('interfaz1.html', mensaje='No puedes enviar un texto vacío.') #AQUI



@main_bp.route("/new_chat", methods=['POST'])
def new_chat():
    create_chat("Nuevo Chat") # Esto tenemos que cambiarlo    
