import json
from pathlib import Path
DATA_PATH = Path(__file__).resolve().parent.parent.parent / "datos" / "users" / "users.json"

class User():
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username


def load_users():
    """Carga los usuarios desde el archivo JSON.

    Returns:
        JSON: Todos los usuarios
    """
    with open(DATA_PATH, 'r') as file:
        users = json.load(file)
    return users

def load_user(user_id):
    """Carga usuario desde una id

    Args:
        user_id (int): Identificador del usuario

    Returns:
        User: id y username del usuario
    """
    users = load_users()
        
    for user in users.values():
        if user["id"] == int(user_id):
            return User(user["id"], user["username"])
    return None

def usuario_existe(password, email):
    """Verifica si un usuario existe en la base de datos y devuelve su información si es correcto.

    Args:
        password (text): Contraseña del usuario
        username (text): Correo electrónico del usuario

    Returns: Clase Usuario
        User: id y username del usuario
    """
    users = load_users()
    for user in users.values():
        if user["email"] == email and user["password"] == password:
            return User(user["id"], user["username"])
    return None


def usuario_unico(usuario):
    """Comprobamos que el nombre de usuario no exista en la base de datos

    Args:
        usuario (Text): Nombre del usuario

    Returns:
        Boolean: Sería único ese usuario en la base de datos
    """
    users = load_users()
    for user in users.values():
        if user["username"] == usuario:
            return False
    return True

def email_unico(email):
    """Comprobamos que el email del usuario no exista en la base de datos

    Args:
        email (Text): Email del usuario

    Returns:
        Boolean: Sería único ese email en la base de datos
    """
    users = load_users()
    for user in users.values():
        if user["email"] == email:
            return False
    return True

def crear_nuevo_usuario(user_id, usuario, email, password):
    
    users = load_users()
    user_id = max([int(user_id) for user_id in users.keys()]) + 1
    users[user_id] = {
        "id": user_id,
        "username": usuario,
        "email": email,
        "password": password
    }
    with open(DATA_PATH, 'w') as file:
        json.dump(users, file, indent=4)
    return True