import sys
import os

# Sube un nivel (de api/ a model/) y agrégalo al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))        # .../model/api
parent_dir = os.path.dirname(current_dir)                       # .../model
sys.path.append(parent_dir)

import openai
from config import config as cfg
from utils.expenditure import update_expenditure
from embeddings import ConversationManager

client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

# Colores para poder leer la salida
GREEN = "\033[92m"
MAGENTA = "\033[35m"
RESET = "\033[0m" 

def chat_with_claude_embeddings():
    # Inicializar el gestor de conversación con la ruta correcta
    conversation_manager = ConversationManager(cfg.CSV_PATH)
    
    print(f"¡Bienvenido al chat con Claude! (Usando modelo: {cfg.ACTIVE_MODEL})")
    print("(Escribe 'salir' para terminar)")
    
    while True:
        # Obtener input del usuario
        user_input = input("\nTú: ")
        
        # Comprobar si el usuario quiere salir
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("¡Adiós!")
            break
        
        # Añadir mensaje del usuario al historial
        conversation_manager.add_message("user", user_input)
        
        # Preparar mensajes para la API incluyendo solo contexto relevante
        messages = conversation_manager.prepare_messages_for_api(user_input)
        print(f"{MAGENTA}PROMPT:{RESET} {GREEN}{messages}{RESET}")
        
        # Realizar la llamada a la API
        try:
            response = client.chat.completions.create(
                model=cfg.ACTIVE_MODEL,
                messages=messages
            )
            
            # Extraer solo el mensaje de respuesta
            assistant_response = response.choices[0].message.content
            
            # Guardar información de uso correctamente
            print(f"{MAGENTA}INPUT: {response.usage.prompt_tokens}, OUTPUT: {response.usage.completion_tokens}{RESET}")
            update_expenditure(response.usage.prompt_tokens, response.usage.completion_tokens)
            
            # Añadir respuesta del asistente al historial
            conversation_manager.add_message("assistant", assistant_response)
            
            # Mostrar la respuesta
            print("\nClaude:", assistant_response)
        except Exception as e:
            print(f"Error en la llamada a la API: {e}")

if __name__ == "__main__":
    chat_with_claude_embeddings()