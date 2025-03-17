import sys
import os

# Sube un nivel (de api/ a model/) y agrégalo al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))        # .../model/api
parent_dir = os.path.dirname(current_dir)                       # .../model
sys.path.append(parent_dir)

import openai
from model.config import config as cfg
from model.utils.expenditure import update_expenditure
from model.api.rag import ConversationManager
from rich.live import Live
from rich.markdown import Markdown
from rich.console import Console
from rich.spinner import Spinner
from datetime import datetime

client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

# Colores para poder leer la salida
GREEN = "\033[92m"
MAGENTA = "\033[35m"
RESET = "\033[0m" 
BLUE = "\033[94m"
console = Console()

def generate_chat_title(user_input):
    """
    Generates a concise title (4-5 words max) for a chat based on the first user message.
    
    Args:
        user_input (str): The first message from the user.
        
    Returns:
        str: A short title for the chat, or a default title if generation fails.
    """
    try:
        # Create a specific system prompt for title generation
        messages = [
            {
                "role": "system", 
                "content": cfg.TITLE_PROMPT
            },
            {"role": "user", "content": user_input}
        ]
        print(messages)
        # Make API call with minimal tokens
        response = client.chat.completions.create(
            model=cfg.ACTIVE_MODEL,
            messages=messages,
            max_tokens=100  # Limiting tokens since we only need a short title
        )
        
        # Extract and clean the title
        title = response.choices[0].message.content.strip()

        # Log token usage but don't update expenditure for internal function
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        print(f"Title generation - Input: {prompt_tokens}, Output: {completion_tokens} tokens")
        
        return title
    except Exception as e:
        print(f"Error generating chat title (API Claude): {str(e)}")
        
        # Return a timestamp-based title as fallback
        return f"{datetime.now().strftime('%d/%m %H:%M')}"

def generate_response(conversation_history, user_input, csv_path=cfg.CSV_PATH):
    """
    Generates an AI response based on the conversation history and user input.
    This function manages the conversation context, retrieves relevant information
    from a CSV knowledge base, and interacts with the OpenAI API to generate
    a contextually appropriate response.
    Args:
        conversation_history (list): A list of dictionaries containing previous
            messages in the conversation, each with 'role' and 'content' keys.
        user_input (str): The current message from the user.
        csv_path (str, optional): Path to the CSV knowledge base file.
            Defaults to the path specified in the config file.
    Returns:
        dict: A dictionary containing:
            - response (str): The AI-generated response.
            - prompt_tokens (int): Number of tokens in the prompt.
            - completion_tokens (int): Number of tokens in the completion.
            - relevant_context (str): The context information used for the response.
            - error (str, optional): Error message if an exception occurs.
    Raises:
        Various exceptions may be caught internally and returned as part of the
        response dictionary with an 'error' key.
    """

    try:
        # Inicializar el gestor de conversación
        print(csv_path)
        conversation_manager = ConversationManager(csv_path)
        
        # Cargar historial previo si existe
        if conversation_history:
            for message in conversation_history:
                conversation_manager.add_message(message["role"], message["content"])
        
        # Añadir mensaje actual del usuario
        conversation_manager.add_message("user", user_input)
        
        # Preparar mensajes para la API con contexto relevante
        messages = conversation_manager.prepare_messages_for_api(user_input)
        
        # Realizar la llamada a la API
        response = client.chat.completions.create(
            model=cfg.ACTIVE_MODEL,
            messages=messages
        )
        
        # Extraer la respuesta
        assistant_response = response.choices[0].message.content
        
        # Actualizar estadísticas de uso
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        update_expenditure(prompt_tokens, completion_tokens)
        
        # Extraer el contexto relevante (opcional, para debugging)
        # Esto asume que el contexto está en el último mensaje del sistema
        relevant_context = ""
        for msg in messages:
            if msg["role"] == "system" and "---" in msg["content"]:
                relevant_context = msg["content"].split("---", 1)[1]
                
        return {
            "response": assistant_response,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "relevant_context": relevant_context
        }
        
    except Exception as e:
        return {
            "error": f"Error generando respuesta (API Claude): {str(e)}",
            "response": "Lo siento, ha ocurrido un error al procesar tu consulta."
        }

def chat_in_console():
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
        print(f"{BLUE}{messages}{RESET}")
        
        # Realizar la llamada a la API con streaming
        try:
            print()
            print("Claude:")

            # Mostrar un spinner mientras esperamos la primera respuesta
            with Live(Spinner("dots"), refresh_per_second=10) as live:
                # Iniciar stream
                stream = client.chat.completions.create(
                    model=cfg.ACTIVE_MODEL,
                    messages=messages,
                    stream=True
                )
                
                # Obtener el primer fragmento (esto bloqueará hasta que llegue)
                first_chunk = next(stream, None)
                
            # Limpiar la línea del spinner
            print("\r" + " " * 30 + "\r", end="")
            
            # Procesar el primer fragmento si existe
            full_response = ""
            if first_chunk and hasattr(first_chunk.choices[0], 'delta') and first_chunk.choices[0].delta.content:
                content = first_chunk.choices[0].delta.content
                full_response += content
            
            # Ahora usar Rich Live para el resto de fragmentos con markdown
            with Live(Markdown(full_response), refresh_per_second=10) as live:
                # Procesar el resto del stream
                for chunk in stream:
                    if hasattr(chunk.choices[0], 'delta') and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        
                        # Actualizar el renderizado de markdown con cada nuevo fragmento
                        live.update(Markdown(full_response))
            
            # Añadir respuesta completa al historial
            conversation_manager.add_message("assistant", full_response)
            
            # No necesitamos renderizar al final porque ya se mostró con formato

        except Exception as e:
            print(f"Error en la llamada a la API de Claude: {e}")

if __name__ == "__main__":
    chat_in_console()
    #print(generate_chat_title("Un homme de 35 ans s'est présenté avec des douleurs thoraciques, de la toux et de la fièvre. Veuillez fournir des suggestions de diagnostic et de traitement possibles."))