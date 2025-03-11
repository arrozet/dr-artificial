import openai # openai v1.0.0+
from api_key.private_key import API_KEY
from expenditure.expenditure import update_expenditure

client = openai.OpenAI(api_key=API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

def chat_with_claude():
    # Mantener el historial de conversación
    messages = []
    
    print("¡Bienvenido al chat con Claude! (Escribe 'salir' para terminar)")
    
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
        response = client.chat.completions.create(
            model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
            messages=messages
        )
        
        # Extraer solo el mensaje de respuesta
        assistant_response = response.choices[0].message.content


        # Guardar información de uso correctamente
        # Esto es una cutrada, ya que llama a la función tras cada mensaje de claude, lo cual no es muy eficiente
        print(f"PROMPT: {response.usage.prompt_tokens}, ANSWER: {response.usage.completion_tokens}")
        update_expenditure(response.usage.prompt_tokens, response.usage.completion_tokens)


        # Añadir respuesta del asistente al historial
        messages.append({"role": "assistant", "content": assistant_response})
        
        # Mostrar la respuesta
        print("\nClaude:", assistant_response)

if __name__ == "__main__":
    chat_with_claude()