import sys
import os

# Sube un nivel (de api/ a model/) y agrégalo al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))        # .../model/api
parent_dir = os.path.dirname(current_dir)                       # .../model
sys.path.append(parent_dir)

import openai
import pandas as pd
import numpy as np
from config import config as cfg
from utils.csv import load_csv_context
from sklearn.metrics.pairwise import cosine_similarity
import json
import requests

client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

class ConversationManager:
    def __init__(self, data_directory, embedding_model="bedrock/amazon.titan-embed-text-v2:0", max_context_messages=10, chunk_size=100):
        self.data_directory = data_directory
        self.embedding_model = embedding_model
        self.max_context_messages = max_context_messages
        self.chunk_size = chunk_size  # Tamaño para dividir el texto en chunks
        self.df = None
        self.text_chunks = []  # Almacenará los fragmentos de texto
        self.df_embeddings = []  # Almacenará los embeddings de cada chunk
        self.conversation_history = []
        self.load_and_embed_all_csvs()
    
    def load_and_embed_all_csvs(self):
        """Cargar todos los CSV del directorio y generar embeddings"""
        try:
            # Usar load_csv_context para obtener todo el contexto combinado
            full_context = load_csv_context(self.data_directory)
            
            if not full_context:
                print("No se pudo cargar el contexto de los CSVs")
                return False
            
            # Dividir el contexto completo en chunks para procesar
            self.text_chunks = self._split_into_chunks(full_context)
            print(f"Contexto dividido en {len(self.text_chunks)} fragmentos")
            
            # Generar embeddings para cada fragmento de texto
            self.df_embeddings = self.get_embeddings(self.text_chunks)
            print(f"Embeddings generados: {len(self.df_embeddings)} fragmentos procesados")
            return True
        except Exception as e:
            print(f"Error al cargar o procesar los CSVs: {e}")
            return False
    
    def _split_into_chunks(self, text):
        """Divide el texto en fragmentos basados en filas de CSV"""
        chunks = []
        
        # Buscar secciones que corresponden a CSVs diferentes
        csv_sections = text.split("CSV Data Context from ")
        
        # Eliminar la primera sección vacía si existe
        if csv_sections and not csv_sections[0].strip():
            csv_sections = csv_sections[1:]
        
        # Procesar cada sección de CSV
        for section in csv_sections:
            if not section.strip():
                continue
                
            # Separar la primera línea (nombre del archivo) del resto
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            csv_name = lines[0]
            
            # Las primeras líneas suelen ser el encabezado
            header_end = 2  # Ajustar según sea necesario
            
            # Cada línea después del encabezado es posiblemente una fila
            for i in range(header_end, len(lines)):
                line = lines[i].strip()
                if line and not line.startswith('-'):  # Ignorar líneas de separación
                    # Creamos un chunk que incluye información sobre el origen del CSV
                    chunk = f"Del archivo {csv_name}:\n{line}"
                    chunks.append(chunk)
        
        print(f"Se crearon {len(chunks)} chunks a partir de las filas de CSV")
        return chunks
    
    def get_embeddings(self, texts):
        """Obtener embeddings para una lista de textos"""
        embeddings = []
        
        for text in texts:
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {cfg.API_KEY}"
                }
                
                payload = {
                    "model": self.embedding_model,
                    "input": text
                }
                
                response = requests.post(
                    f"{client.base_url}/embeddings",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    embeddings.append(result["data"][0]["embedding"])
                else:
                    print(f"Error en solicitud: {response.status_code} - {response.text}")
                    # Fallback a un vector de ceros
                    embeddings.append([0.0] * 1536)
            except Exception as e:
                print(f"Error generando embedding: {e}")
                embeddings.append([0.0] * 1536)
                
        return embeddings
    
    def add_message(self, role, content):
        """Añadir un mensaje al historial de conversación"""
        self.conversation_history.append({"role": role, "content": content})
    
    def get_relevant_context(self, query, top_k=3):
        """Encontrar los fragmentos de texto más relevantes para la consulta actual"""
        # Obtener embedding para la consulta
        query_embedding = self.get_embeddings([query])[0]
        
        # Calcular similitud con todos los fragmentos
        similarities = [cosine_similarity([query_embedding], [emb])[0][0] for emb in self.df_embeddings]
        
        # Obtener los índices de los fragmentos más similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Generar contexto con los fragmentos más relevantes
        relevant_context = ""
        for idx in top_indices:
            relevant_context += f"--- Fragmento {idx+1} (Similitud: {similarities[idx]:.4f}) ---\n"
            relevant_context += f"{self.text_chunks[idx]}\n\n"
        
        return relevant_context
    
    def prepare_messages_for_api(self, current_query):
        """Preparar mensajes para enviar a la API, incluyendo contexto relevante"""
        # Obtener contexto relevante de los CSVs
        relevant_context = self.get_relevant_context(current_query)
        
        # Crear mensaje del sistema con el contexto relevante
        system_message = {
            "role": "system", 
            "content": f"{cfg.PROMPT} {relevant_context}"
        }
        
        # Incluir mensajes recientes del historial (límite para ahorrar tokens)
        recent_messages = self.conversation_history[-self.max_context_messages:] if len(self.conversation_history) > self.max_context_messages else self.conversation_history
        
        # Crear lista final de mensajes
        messages = [system_message] + recent_messages
        
        return messages