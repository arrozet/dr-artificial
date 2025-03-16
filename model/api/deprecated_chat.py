import sys
import os

# Sube un nivel (de api/ a model/) y agrégalo al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))        # .../model/api
parent_dir = os.path.dirname(current_dir)                       # .../model
sys.path.append(parent_dir)

import openai # openai v1.0.0+
import pandas as pd
from config import config as cfg
from utils.csv import load_csv_context
from utils.expenditure import update_expenditure


client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")



def chat_with_claude():
    # Mantener el historial de conversación
    messages = []
    
    # Cargar contexto CSV
    csv_context = load_csv_context(cfg.CSV_PATH)
    
    if csv_context:
        # Añadir el contexto como primer mensaje del sistema
        system_message = {
            "role": "system", 
            "content": f"A continuación se proporciona un conjunto de datos para referencia en la conversación:\n\n{csv_context}"
        }
        messages.append(system_message)
    
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
        messages.append({"role": "user", "content": user_input})
        
        # Realizar la llamada a la API
        try:
            response = client.chat.completions.create(
                model=cfg.ACTIVE_MODEL,
                messages=messages
            )
            
            # Extraer solo el mensaje de respuesta
            assistant_response = response.choices[0].message.content

            # Guardar información de uso correctamente
            print(f"PROMPT: {response.usage.prompt_tokens}, ANSWER: {response.usage.completion_tokens}")
            update_expenditure(response.usage.prompt_tokens, response.usage.completion_tokens)

            # Añadir respuesta del asistente al historial
            messages.append({"role": "assistant", "content": assistant_response})
            
            # Mostrar la respuesta
            print("\nClaude:", assistant_response)
        except Exception as e:
            print(f"Error en la llamada a la API: {e}")

if __name__ == "__main__":
    chat_with_claude()