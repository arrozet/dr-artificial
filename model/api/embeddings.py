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
import hashlib
from datetime import datetime
import pickle
import re

RESET = "\033[0m" 
YELLOW = "\033[33m"

client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

class ConversationManager:
    def __init__(self, data_directory, embedding_model="bedrock/amazon.titan-embed-text-v2:0", max_context_messages=10, chunk_size=100):
            """
            Initialize the embedding processor.
            This class handles the processing, embedding, and caching of text data from CSV files.
            Parameters:
            ----------
            data_directory : str
                Path to the directory containing CSV files to process
            embedding_model : str, default="bedrock/amazon.titan-embed-text-v2:0"
                Name of the embedding model to use
            max_context_messages : int, default=10
                Maximum number of conversation messages to maintain in context
            chunk_size : int, default=100
                Size of text chunks for embedding processing
            Attributes:
            ----------
            df : pandas.DataFrame
                Dataframe containing the processed data
            text_chunks : list
                List of text chunks extracted from the data
            df_embeddings : list
                List of embeddings generated from text chunks
            conversation_history : list
                History of conversation messages
            cache_dir : str
                Directory where embeddings are cached
            embeddings_cache_file : str
                File path for cached embeddings
            """
            self.data_directory = data_directory
            self.embedding_model = embedding_model
            self.max_context_messages = max_context_messages
            self.chunk_size = chunk_size
            
            self.df = None
            self.text_chunks = []
            self.df_embeddings = []
            self.conversation_history = []
            
            # Ruta donde guardaremos los embeddings
            self.cache_dir = os.path.join(parent_dir, "cache")
            os.makedirs(self.cache_dir, exist_ok=True)
            
            # Nombre de archivo de cache basado en el modelo de embedding
            self.embeddings_cache_file = os.path.join(
                self.cache_dir, 
                f"embeddings_{self.embedding_model.replace('/', '_').replace('.', '__').replace(':', '--')}.pkl"
            )
            
            # Cargar embeddings o calcular nuevos si es necesario
            if not self.load_cached_embeddings():
                print("Calculando embeddings...")
                self.load_and_embed_all_csvs()
    
    def get_data_hash(self):
        """Genera un hash de los archivos CSV para detectar cambios"""
        hash_value = hashlib.md5()
        
        for root, _, files in os.walk(self.data_directory):
            for file in sorted(files):
                if file.endswith('.csv'):
                    filepath = os.path.join(root, file)
                    mtime = os.path.getmtime(filepath)
                    hash_value.update(f"{filepath}:{mtime}".encode())
                    
        return hash_value.hexdigest()
    
    def load_cached_embeddings(self):
        """
        Attempts to load previously calculated embeddings from the cache file.
        This method tries to load text chunks and their corresponding embeddings from a
        previously saved cache file. It also verifies if the source data has changed since
        the embeddings were calculated by comparing hash values.
        Returns:
            bool: True if embeddings were successfully loaded from cache, False otherwise.
                  Returns False in the following cases:
                  - Cache file doesn't exist
                  - Source data has changed (different hash value)
                  - Any error occurs during the loading process
        """
        try:
            if not os.path.exists(self.embeddings_cache_file):
                print("No se encontró caché de embeddings")
                return False
                
            with open(self.embeddings_cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Verificar si los datos han cambiado desde que se calcularon los embeddings
            if cache_data.get('data_hash') != self.get_data_hash():
                print("Los datos han cambiado desde el último cálculo de embeddings")
                return False
                
            # Cargar datos del caché
            self.text_chunks = cache_data['text_chunks']
            self.df_embeddings = cache_data['embeddings']
            
            print(f"Embeddings cargados desde caché: {len(self.df_embeddings)} fragmentos")
            return True
            
        except Exception as e:
            print(f"Error al cargar embeddings en caché: {e}")
            return False
            
    def save_embeddings_cache(self):
        """Guarda embeddings calculados para uso futuro"""
        try:
            cache_data = {
                'data_hash': self.get_data_hash(),
                'text_chunks': self.text_chunks,
                'embeddings': self.df_embeddings,
                'timestamp': datetime.now().isoformat()
            }
            
            with open(self.embeddings_cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
                
            print(f"Embeddings guardados en caché: {self.embeddings_cache_file}")
            return True
            
        except Exception as e:
            print(f"Error al guardar embeddings en caché: {e}")
            return False
    
    def load_and_embed_all_csvs(self):
        """
        Load all CSVs from the data directory and generate embeddings.
        
        This method reads all CSV files from the data directory, processes them
        into text chunks, and then generates vector embeddings for each chunk.
        The resulting embeddings are cached for future use.
        
        Returns:
            bool: True if the process completes successfully, False otherwise.
        """
        try:
            # Código existente para cargar y procesar CSVs
            full_context = load_csv_context(self.data_directory)
            
            if not full_context:
                print("No se pudo cargar el contexto de los CSVs")
                return False
            
            # Dividir y generar embeddings
            self.text_chunks = self._split_into_chunks(full_context)
            print(f"Contexto dividido en {len(self.text_chunks)} fragmentos")
            
            self.df_embeddings = self.get_embeddings(self.text_chunks)
            print(f"Embeddings generados: {len(self.df_embeddings)} fragmentos procesados")
            
            # Guardar en caché para uso futuro
            self.save_embeddings_cache()
            
            return True
        except Exception as e:
            print(f"Error al cargar o procesar los CSVs: {e}")
            return False
    
    def _split_into_chunks(self, text):
        """
        Splits text into chunks based on CSV rows.
        This method processes text containing CSV data by identifying different 
        CSV sections, extracting the file names, and creating individual chunks 
        for each data row. It ignores empty sections, separator lines, and creates 
        chunks that include information about the source CSV file.
        
        Additionally, it writes debug information about all created chunks to a 
        file in the cache directory for development and troubleshooting purposes.
        
        Args:
            text (str): The input text containing CSV data sections prefixed with the CONTEXT_PREFIX
        Returns:
            list: A list of string chunks where each chunk contains a CSV row prefixed with its source file information
        Note:
            - CSV sections are identified by the CONTEXT_PREFIX
            - The method assumes the first line contains header information
            - Separator lines (starting with '-') are ignored
            - Row numbers are automatically removed from the beginning of each line
            - Debug information is saved to chunks_debug.txt in the cache directory
        """
        chunks = []
        
        # Para debuggear la creacion de chunks
        chunks_file_path = os.path.join(self.cache_dir, "chunks_debug.txt")

        
        # Buscar secciones que corresponden a CSVs diferentes
        csv_sections = text.split(cfg.CONTEXT_PREFIX)
        
        # Eliminar la primera sección vacía si existe
        if csv_sections and not csv_sections[0].strip():
            csv_sections = csv_sections[1:]
        
        # Abrir archivo para guardar chunks
        with open(chunks_file_path, 'w', encoding='utf-8') as f:
            f.write(f"=== CHUNKS GENERADOS: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
            
            # Procesar cada sección de CSV
            for section in csv_sections:
                if not section.strip():
                    continue
                    
                # Separar la primera línea (nombre del archivo) del resto
                lines = section.strip().split('\n')
                if not lines:
                    continue
                    
                # Extraer el nombre del archivo CSV, quitando la parte 'data/'
                csv_name = lines[0]
                if '/' in csv_name:
                    csv_name = csv_name.split('data/', 1)[1] if 'data/' in csv_name else csv_name
                    csv_name = re.sub(r'\s+', ' ', csv_name)
                
                # Las primeras líneas suelen ser el encabezado
                header_end = 1  # Ajustar según sea necesario
                
                # Cada línea después del encabezado es posiblemente una fila
                for i in range(header_end, len(lines)):
                    line = lines[i].strip()
                    if line and not line.startswith('-'):  # Ignorar líneas de separación
                        # Eliminar el índice de fila (primer número seguido de espacios)
                        line = re.sub(r'^\d+\s+', '', line)
                        
                        # Normalizar espacios múltiples a uno solo
                        line = re.sub(r'\s+', ' ', line)

                        # Creamos un chunk que incluye información sobre el origen del CSV
                        chunk = f"{csv_name}:{line}"
                        
                        # Guardar chunk en archivo
                        f.write(f"--- CHUNK #{len(chunks) + 1} ---\n")
                        f.write(chunk)
                        f.write("\n\n" + "=" * 50 + "\n\n")
                        
                        # Añadir a la lista
                        chunks.append(chunk)
            
            print(f"Se crearon {len(chunks)} chunks a partir de las filas de CSV")
            return chunks
    
    def get_embeddings(self, texts):
        """
        Generate embeddings for a list of texts using the specified embedding model.
        The method makes API calls to create vector representations for each text.
        If an error occurs during the API call or processing, a fallback vector
        of zeros with 1536 dimensions is used instead.
        Args:
            texts (list): A list of strings for which to generate embeddings
        Returns:
            list: A list of embedding vectors, where each vector is a list of floats.
                  Each vector corresponds to the input text at the same index.
        Raises:
            No exceptions are raised as errors are caught internally and fallback
            vectors are provided instead.
        """
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
                    embeddings.append([0.0] * cfg.OUTPUT_VECTOR_SIZE)
            except Exception as e:
                print(f"Error generando embedding: {e}")
                embeddings.append([0.0] * cfg.OUTPUT_VECTOR_SIZE)
                
        return embeddings
    
    def add_message(self, role, content):
        """
        Add a message to the conversation history.
        
        Parameters:
        -----------
        role : str
            The role of the message sender (e.g., 'user', 'assistant', 'system').
        content : str
            The content of the message.
        
        Returns:
        --------
        None
            The message is appended to the conversation history.
        """
        self.conversation_history.append({"role": role, "content": content})
    
    def get_relevant_context(self, query, top_k=5):
        """
        Retrieves the most relevant text chunks for a given query using cosine similarity.
        This method computes the embedding for the input query and finds the most 
        similar text chunks by comparing their embeddings through cosine similarity.
        Parameters:
        -----------
        query : str
            The query text for which to find relevant context
        top_k : int, default=5
            The number of most relevant chunks to return
        Returns:
        --------
        str
            Formatted string containing the top_k most relevant text chunks
            with their similarity scores, separated by chunk identifiers
        """
        # Obtener embedding para la consulta
        query_embedding = self.get_embeddings([query])[0]
        
        # Calcular similitud con todos los fragmentos
        similarities = [cosine_similarity([query_embedding], [emb])[0][0] for emb in self.df_embeddings]
        
        # Obtener los índices de los fragmentos más similares
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Generar contexto con los fragmentos más relevantes
        relevant_context = ""
        for idx in top_indices:
            print(YELLOW + f"--- Fragmento {idx+1} (Similitud: {similarities[idx]:.4f}) ---" + RESET)
            relevant_context += f"--- {self.text_chunks[idx]}--- "
        
        return relevant_context
    
    def prepare_messages_for_api(self, current_query):
        """
        Prepares messages to send to the API, including relevant context from the conversation history.
        This method generates a structured message payload for the API by:
        1. Retrieving relevant context based on the current query
        2. Creating a system message that includes the prompt and context
        3. Adding recent conversation history messages (limited to save tokens)
        Parameters:
        -----------
        current_query : str
            The current user query to process
        Returns:
        --------
        list
            A list of message objects formatted for the API, including the system message
            with context and recent conversation history
        """
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