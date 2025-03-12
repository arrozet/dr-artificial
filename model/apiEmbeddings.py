import openai
import pandas as pd
import numpy as np
from api_key.private_key import API_KEY
from expenditure.expenditure import update_expenditure
from config import ACTIVE_MODEL
from sklearn.metrics.pairwise import cosine_similarity

client = openai.OpenAI(api_key=API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

class ConversationManager:
    def __init__(self, csv_path, embedding_model="bedrock/amazon.titan-embed-text-v2:0", max_context_messages=10):
        self.csv_path = csv_path
        self.embedding_model = embedding_model
        self.max_context_messages = max_context_messages
        self.df = None
        self.df_embeddings = None
        self.conversation_history = []
        self.load_and_embed_csv()
    
    def load_and_embed_csv(self):
        """Cargar el CSV y generar embeddings para cada fila"""
        try:
            # Cargar el CSV
            self.df = pd.read_csv("datos\\r_dataton\\datos_sinteticos\\resumen_pacientes.csv")
            
            # Generar representaciones textuales de cada fila
            text_representations = []
            for _, row in self.df.iterrows():
                text = " ".join([f"{col}: {val}" for col, val in row.items()])
                text_representations.append(text)
            
            # Generar embeddings para cada representación de texto
            self.df_embeddings = self.get_embeddings(text_representations)
            print(f"CSV cargado y embeddings generados: {len(self.df_embeddings)} filas procesadas")
            return True
        except Exception as e:
            print(f"Error al cargar o procesar el CSV: {e}")
            return False
    
    def get_embeddings(self, texts):
        """Obtener embeddings para una lista de textos"""
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                model=self.embedding_model,
                input=text  # No pasamos encoding_format explícitamente
            )
            embeddings.append(response.data[0].embedding)
        return embeddings
    
    def add_message(self, role, content):
        """Añadir un mensaje al historial de conversación"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_relevant_csv_context(self, query, top_k=5):
        """Encontrar las filas más relevantes del CSV para la consulta actual"""
        # Obtener embedding para la consulta
        query_embedding = self.get_embeddings([query])[0]
        
        # Calcular similitud con todas las filas
        similarities = [cosine_similarity([query_embedding], [emb])[0][0] for emb in self.df_embeddings]
        
        # Obtener los índices de las filas más similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Generar contexto con las filas más relevantes
        relevant_rows = self.df.iloc[top_indices]
        return f"Datos relevantes del CSV:\n{relevant_rows.to_string()}\n\n"
    
    def prepare_messages_for_api(self, current_query):
        """Preparar mensajes para enviar a la API, incluyendo contexto relevante"""
        # Obtener contexto relevante del CSV
        relevant_context = self.get_relevant_csv_context(current_query)
        
        # Crear mensaje del sistema con el contexto relevante
        system_message = {
            "role": "system",
            "content": f"A continuación se proporciona un conjunto de datos relevantes para la consulta actual:\n\n{relevant_context}"
        }
        
        # Incluir mensajes recientes del historial (límite para ahorrar tokens)
        recent_messages = self.conversation_history[-self.max_context_messages:] if len(self.conversation_history) > self.max_context_messages else self.conversation_history
        
        # Crear lista final de mensajes
        messages = [system_message] + recent_messages
        
        return messages

def chat_with_claude_embeddings():
    # Inicializar el gestor de conversación
    conversation_manager = ConversationManager("datos\\r_dataton\\datos_sinteticos\\resumen_pacientes.csv")
    
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
        conversation_manager.add_message("user", user_input)
        
        # Preparar mensajes para la API incluyendo solo contexto relevante
        messages = conversation_manager.prepare_messages_for_api(user_input)
        
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
            conversation_manager.add_message("assistant", assistant_response)
            
            # Mostrar la respuesta
            print("\nClaude:", assistant_response)
        except Exception as e:
            print(f"Error en la llamada a la API: {e}")

if __name__ == "__main__":
    chat_with_claude_embeddings()