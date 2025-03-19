from flask import Blueprint, jsonify, render_template, request, session, redirect
import os
import sys

# Configuración de rutas para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))  # routes folder
app_dir = os.path.dirname(current_dir)                    # app folder
web_dir = os.path.dirname(app_dir)                        # web folder
project_root = os.path.dirname(web_dir)                   # project root

# Configuración de rutas para importaciones
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar funciones específicas para manejo de chats
from web.utils.chat_handler import (
    list_of_chats,
    list_of_messages,
    add_message,
    create_chat,
    delete_chat
)

# Importar funciones específicas para manejo de usuarios
from web.utils.usuarios_handler import (
    usuario_existe,
    usuario_unico,
    email_unico,
    crear_nuevo_usuario
)

# Importar funciones del modelo de IA
from model.api.chat import generate_response, generate_default_prompts, generate_chat_title


main_bp = Blueprint("main", __name__)

# Manejo de datos de datos temporales
datos_guardados = {"chat_id": 0}

def procesarNuevoMensaje( chat_id, prompt, user_id):
    """
    Procesa un nuevo mensaje del usuario y genera una respuesta con la IA.
    
    Args:
        chat_id (int): ID del chat actual, 0 si es un chat nuevo
        prompt (str): Mensaje del usuario
        user_id (int): ID del usuario
        
    Returns:
        int: ID del chat procesado
    """
    
    # Crear un nuevo chat si es necesario
    if chat_id == 0:            
            
        nombre_chat = generate_chat_title(prompt)
        chat_id = create_chat(nombre_chat, user_id)
        datos_guardados["chat_id"] = chat_id
        
    # Añadir el mensaje del usuario al chat
    add_message(chat_id=chat_id, text=prompt, sender="usuario", id_usuario=user_id)
        
    # Obtener los mensajes anteriores para construir el historial de conversación
    mensajes_anteriores = list_of_messages(chat_id, user_id)
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
                
    add_message(chat_id=chat_id, text=ia_response, sender="IA", id_usuario=user_id) 
    
    return chat_id   

@main_bp.route("/")
def home():
    """
    Ruta principal que renderiza la página inicial.
    Returns:
        str: Template HTML renderizado con la lista de chats
    """
    
    # Si no hay usuario logueado, redirigir a la página de login
    if not session.get("user_id"):
        return redirect("login.html")
    
    # Cargamos las variables necesarias
    user_id = session.get("user_id")
    chat_id = datos_guardados["chat_id"]
    
    # Cargamos los chats
    chat_list = list_of_chats(user_id)        
    mensajes_chat = []
    msg1,msg2,msg3,msg4 = None,None,None,None
    
        
    # Cargamos todos los mensajes del chat
    mensajes_chat = list_of_messages(chat_id, user_id)
    if mensajes_chat == []:     # Si no hay mensajes, estamos ante un nuevo chat, generamos los mensajes por defecto
        prompt_list = generate_default_prompts()
        msg1 = prompt_list[0]
        msg2 = prompt_list[1]
        msg3 = prompt_list[2]
        msg4 = prompt_list[3]
        
    
    
    return render_template("index.html",
                            chat_list=chat_list, 
                            mensajes_nuevo_chat=mensajes_chat, 
                            chat_id=0, 
                            username=session.get("username"),
                            msg1=msg1,
                            msg2=msg2,
                            msg3=msg3,
                            msg4=msg4)

@main_bp.route('/', methods=['GET','POST'])
def procesarPeticiones():
    """
    Procesa las peticiones POST de la interfaz web: nuevos mensajes, 
    borrado de chats, y cambios entre chats.
    
    Returns:
        str: Template HTML parcial con los datos actualizados
    """
    # Si no hay usuario logueado, redirigir a la página de login
    if not session.get("user_id"):
        return redirect("login.html")
    
    data = request.get_json()                       # Cargamos el JSON
    
    chat_id = data.get("chat_id", datos_guardados["chat_id"])             
    prompt = data.get('prompt', None)                
    borrar_chat_id = data.get("borrar_chat_id", None)
    user_id = session.get("user_id")
    msg1,msg2,msg3,msg4 = None,None,None,None

    if prompt:                     # Por tanto la petición es de un nuevo mensaje
        
        chat_id = procesarNuevoMensaje(chat_id, prompt, user_id)

        
    elif borrar_chat_id:    # La petición es sobre borrar un chat
        delete_chat(borrar_chat_id,user_id)
        
        if int(chat_id) == int(borrar_chat_id):
            chat_id = 0
        
    else:                       # La petición es de cargar un chat existente
        
        chat_id = data.get("chat_id")        
        datos_guardados["chat_id"] = chat_id
       
       
    chat_list = list_of_chats(user_id)
    mensajes_chat = list_of_messages(chat_id, user_id)
     
    if mensajes_chat == []:     # Si no hay mensajes, estamos ante un nuevo chat, generamos los mensajes por defecto
        prompt_list = generate_default_prompts()
        msg1 = prompt_list[0]
        msg2 = prompt_list[1]
        msg3 = prompt_list[2]
        msg4 = prompt_list[3]    

    return render_template('index_body.html',
                           chat_list=chat_list,
                           mensajes_nuevo_chat=mensajes_chat,
                           chat_id=chat_id,
                           username=session.get("username"),
                           msg1=msg1,
                           msg2=msg2,
                           msg3=msg3,
                           msg4=msg4)

@main_bp.route('/<chat_name>')
def mostrar_chat(chat_name: str):
    """
    Ruta para mostrar un chat específico (placeholder).
    
    Args:
        chat_name: Nombre del chat a mostrar
    Returns:
        str: Template HTML del chat
    """
    return render_template(f'{chat_name}')



@main_bp.route('/login', methods=['POST'])
def login():
    """Función que maneja el inicio de sesión de un usuario."""
    # Obtenemos los datos de la request    
    data = request.get_json()
    password = data.get("password", None)
    email = data.get("email", None)
    remember = data.get("remember", False)
    
    # Comprobamos que los datos sean correctos
    if not password or password.strip() == "":
        return jsonify({"message": "La contraseña no puede estar vacía"}), 401
    
    if not email or email.strip() == "":
        return jsonify({"message": "El correo electrónico no puede estar vacío"}), 401

    # Comprobamos que el usuario sea correcto
    user = usuario_existe(password, email)
    if not user:
        return jsonify({"message": "Credenciales incorrectas"}), 403
    
    # Ahora accedemos correctamente a las propiedades del objeto User
    session["user_id"] = user.id
    session["username"] = user.username
    
    return jsonify({
        "message": "Inicio de sesión exitoso", 
        "user_id": user.id, 
        "username": user.username
    }), 200


@main_bp.route('/signup', methods=['POST'])
def register():
    """No se usa en esta versión

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

# Añadir ruta para cerrar sesión
@main_bp.route('/logout')
def logout():
    """Cierra la sesión del usuario"""
    session.clear()
    return redirect("login.html")