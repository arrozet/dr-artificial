import openai # openai v1.0.0+
import pandas as pd
from api_key.private_key import API_KEY
from expenditure.expenditure import update_expenditure
from config import ACTIVE_MODEL

client = openai.OpenAI(api_key=API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

def load_csv_context(file_path):
    """Load CSV file and convert it to a string context"""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Convert to string representation
        context = f"CSV Data Context:\n{df.to_string()}\n\n"
        
        print(f"Loaded context from {file_path} successfully.")
        return context
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

def chat_with_claude():
    # Mantener el historial de conversación
    messages = []
    
    # Cargar contexto CSV
    csv_context = load_csv_context("datos\\r_dataton\\datos_sinteticos\\resumen_pacientes.csv")
    
    if csv_context:
        # Añadir el contexto como primer mensaje del sistema
        system_message = {
            "role": "system", 
            "content": f"A continuación se proporciona un conjunto de datos para referencia en la conversación:\n\n{csv_context}"
        }
        messages.append(system_message)
    
    print(f"¡Bienvenido al chat con Claude! (Usando modelo: {ACTIVE_MODEL})")
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
                model=ACTIVE_MODEL,
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