from flask import Blueprint, jsonify, render_template, request
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

# Import specific functions instead of using wildcard import
from web.utils.usuarios_handler import (
    usuario_existe,
    usuario_unico,
    email_unico,
    crear_nuevo_usuario
)

# Importar el generador de respuestas del modelo
from model.api.chat import generate_response
from model.api.chat import generate_chat_title


main_bp = Blueprint("main", __name__)

datos_guardados = {"chat_id": 0}


@main_bp.route("/")
def home():
    """
    Ruta principal que renderiza la página inicial.
    Returns:
        str: Template HTML renderizado con la lista de chats
    """
    
    # Cargamos todos los chats
    chat_list = list_of_chats()
    
    return render_template("index.html", chat_list=chat_list, mensajes_nuevo_chat=[], chat_id=0)

""" 
Cuando recibe una petición POST la página web, esta función resuelve
"""
@main_bp.route('/', methods=['GET','POST'])
def procesarPeticiones():

    data = request.get_json()                       # Cargamos el JSON
    
    chat_id = data.get("chat_id", datos_guardados["chat_id"])             
    prompt = data.get('prompt', None)                
    borrar_chat_id = data.get("borrar_chat_id", None)
    
    if prompt:                     # Por tanto la petición es de un nuevo mensaje
        
        if chat_id == 0:            # Estamos creando un nuevo chat
            
            # nombre_chat = prompt.split()[0] if prompt.strip() else ""       # HABRÁ QUE CAMBIARLO
            nombre_chat = generate_chat_title(prompt)

            chat_id = create_chat(nombre_chat)
            datos_guardados["chat_id"] = chat_id
        
        # Añadir el mensaje del usuario al chat
        add_message(chat_id=chat_id, text=prompt, sender="usuario")
        
        # Obtener los mensajes anteriores para construir el historial de conversación
        mensajes_anteriores = list_of_messages(chat_id)
        conversation_history = []
        
        # Convertir los mensajes al formato esperado por generate_response
        
        for msg in mensajes_anteriores:
            if msg["message_sender"] == "usuario":
                conversation_history.append({"role": "user", "content": msg["message"]})
            else:
                conversation_history.append({"role": "assistant", "content": msg["message"]})
        
        # Generar respuesta usando el modelo
        try:
            respuesta = generate_response(conversation_history, prompt)
            ia_response = respuesta.get("response", "Lo siento, no puedo procesar tu solicitud en este momento.")
        except Exception as e:
            print(f"Error al generar respuesta: {str(e)}")
            ia_response = "Ha ocurrido un error al procesar tu consulta."
        
        # Añadir la respuesta de la IA al chat
        
        add_message(chat_id=chat_id, text=ia_response, sender="IA")
        
    elif borrar_chat_id:    # La petición es sobre borrar un chat
        delete_chat(borrar_chat_id)
        
        if int(chat_id) == int(borrar_chat_id):
            chat_id = 0
        
    else:                                          # La petición es de cargar un chat existente
        
        chat_id = data.get("chat_id")        
        datos_guardados["chat_id"] = chat_id

    chat_list = list_of_chats()
    mensajes_chat = list_of_messages(chat_id)

    return render_template('index_body.html', chat_list=chat_list, mensajes_nuevo_chat=mensajes_chat, chat_id=chat_id)

@main_bp.route('/<chat_name>')
def mostrar_chat(chat_name: str):
    """
    Ruta para mostrar un chat específico (placeholder).
    
    Args:
        chat_name: Nombre del chat a mostrar
    Returns:
        str: Template HTML del chat
    """
    return render_template(f'{chat_name}.html')



@main_bp.route('/login', methods=['POST'])
def login():
    """Función que maneja el inicio de sesión de un usuario.

    Returns:
        Int, Test: id y nombre del usuario que se ha registrado
    """
    # Obtenemos los datos de la request    
    data = request.get_json()
    password = data.get("password", None)
    email = data.get("email", None)
    
    # Comprobamos que los datos sean correctos
    
    if not password or password.strip() == "":
        return jsonify({"message": "La contraseña no puede estar vacía"}), 401
    
    if not email or email.strip() == "":
        return jsonify({"message": "El correo electrónico no puede estar vacío"}), 401

    # Comprobamos que el usuario sea correcto
    user = usuario_existe(password, email)
    if not user:
        return jsonify({"message": "Credenciales incorrectas"}), 401
    else:
        return jsonify({"message": "Inicio de sesión exitoso", "user_id": user["id"], "username": user["username"]}), 200

@main_bp.route('/register', methods=['POST'])
def register():
    """_summary_

    Returns:
        _type_: _description_
    """
    data = request.get_json()
    username = data.get("username", None)
    password = data.get("password", None)
    email = data.get("email", None)
    
    # Comprobamos que los datos sean correctos
    if not username or username.strip() == "":
        return jsonify({"message": "El nombre de usuario no puede estar vacío"}), 401
    
    if not password or password.strip() == "":
        return jsonify({"message": "La contraseña no puede estar vacía"}), 401
    
    if not email or email.strip() == "":
        return jsonify({"message": "El correo electrónico no puede estar vacío"}), 401
    
    # Comprobamos que el usuario sea único
    if not usuario_unico(username):
        return jsonify({"message": "El nombre de usuario ya está en uso"}), 401
    
    # Comprobamos que el email sea único
    if not email_unico(email):
        return jsonify({"message": "El correo electrónico ya está en uso"}), 401
    
    # Creamos el usuario
    crear_nuevo_usuario(username, password, email)
    
    return jsonify({"message": "Inicio de sesión exitoso"}), 200
