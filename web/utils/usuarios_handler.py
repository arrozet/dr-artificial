import json
from pathlib import Path
DATA_PATH = Path(__file__).resolve().parent.parent.parent / "datos" / "users" / "users.json"

class User():
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
    
def load_users():
    """Carga los usuarios desde el archivo JSON."""
    try:
        
        with DATA_PATH.open("r",encoding="utf8") as file:
            users = json.load(file)
        if isinstance(users, list):
            users_dict = {}
            for user in users:
                if "id" in user:
                    users_dict[str(user["id"])] = user
            
            # Guardar en formato diccionario para futuros usos
            with open(DATA_PATH, 'w') as file:
                json.dump(users_dict, file, indent=4)
            
            return users_dict
            
        return users
    
    except FileNotFoundError:
        # Si el archivo no existe, crear estructura básica
        empty_users = {}
        with open(DATA_PATH, 'w') as file:
            json.dump(empty_users, file, indent=4)
        return empty_users
    except json.JSONDecodeError:
        # Si el JSON está mal formado
        print("Error: Archivo de usuarios corrupto")
        return {}


def load_user(user_id):
    """Carga usuario desde una id

    Args:
        user_id (int): Identificador del usuario

    Returns:
        User: id y username del usuario
    """
    users = load_users()
        
    user_id_str = str(user_id)
    
    if user_id_str in users:
        user = users[user_id_str]
        return User(user["id"], user["username"])
    
    return None

def usuario_existe(password, email):
    """Verifica si un usuario existe en la base de datos y devuelve su información si es correcto."""
    users = load_users()
    
    # Si users es un diccionario (formato esperado)
    for user in users.get("users", []):
        if user.get("email") == email and user.get("password") == password:
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
    """Crea un nuevo usuario verificando que username y email sean únicos"""
    # Validar que el usuario y email sean únicos
    if not usuario_unico(usuario):
        return False, "El nombre de usuario ya existe"
    
    if not email_unico(email):
        return False, "El correo electrónico ya está registrado"
        
    users = load_users()
    
    # Generar nuevo ID (manejo seguro si no hay usuarios)
    if users:
        try:
            user_id = max([int(uid) for uid in users.keys()]) + 1
        except (ValueError, TypeError):
            # Si hay claves no numéricas
            user_id = 1
    else:
        user_id = 1
        
    # Idealmente, hash de contraseña (implementación básica)
    # import hashlib
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    users[str(user_id)] = {
        "id": user_id,
        "username": usuario,
        "email": email,
        "password": password  # Mejor usar hashed_password
    }
    
    with open(DATA_PATH, 'w') as file:
        json.dump(users, file, indent=4)
    
    return True, user_id