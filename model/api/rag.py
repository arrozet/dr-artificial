import sys
import os

# Sube un nivel (de api/ a model/) y agrégalo al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))        # .../model/api
parent_dir = os.path.dirname(current_dir)                       # .../model
sys.path.append(parent_dir)

import openai
import pandas as pd
import numpy as np
from model.config import config as cfg
from model.utils.csv import load_csv_context
from sklearn.metrics.pairwise import cosine_similarity
import json
import requests
import hashlib
from datetime import datetime
import pickle
import re

RESET = "\033[0m" 
YELLOW = "\033[33m"
GREEN = "\033[92m"
MAGENTA = "\033[35m"

client = openai.OpenAI(api_key=cfg.API_KEY, base_url="https://litellm.dccp.pbu.dedalus.com")

class ConversationManager:
    def __init__(self, data_directory, embedding_model="bedrock/amazon.titan-embed-text-v2:0", max_context_messages=10, chunk_size=8000):
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
            chunk_size : int, default=8000
                Maximum number of tokens per chunk (set close to model limit of 8,192)
            
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
                    rel_path = os.path.relpath(filepath, self.data_directory)
                    mtime = os.path.getmtime(filepath)
                    hash_value.update(f"{rel_path}:{mtime}".encode())
                    
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
            print(self.embeddings_cache_file)
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
    
    def _split_into_chunks(self, dataframe_list):
        """
        Splits a list of DataFrames into chunks grouped by PacienteID when possible.
        
        Args:
            dataframe_list (list): List of pandas DataFrames, each with 'source_file' as first column
                
        Returns:
            list: A list of string chunks optimized for context retrieval
        """
        # Primero crear un mapa de pacientes y sus nombres usando todos los DataFrames
        paciente_nombre_map = self._build_patient_name_map(dataframe_list)
        
        chunks = []
        chunks_file_path = os.path.join(self.cache_dir, "chunks_debug.txt")
        
        with open(chunks_file_path, 'w', encoding='utf-8') as f:
            f.write(f"=== CHUNKS GENERADOS: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} ===\n\n")
            
            # Procesar cada DataFrame
            for df in dataframe_list:
                if 'source_file' not in df.columns:
                    continue
                    
                csv_name = df['source_file'].iloc[0] if not df.empty else "unknown"
                
                # Verificar si el DataFrame contiene la columna PacienteID
                has_paciente_id = any(col in df.columns for col in ['PacienteID', 'pacienteid', 'PACIENTEID', 'Paciente_ID', 'ID_Paciente'])
                
                if has_paciente_id:
                    # Procesar DataFrames con PacienteID
                    new_chunks = self._process_df_with_patient_id(df, csv_name, paciente_nombre_map)
                    
                    # Verificar y dividir chunks que exceden el límite de caracteres
                    processed_chunks = self._enforce_chunk_size_limit(new_chunks)
                    
                    chunks.extend(processed_chunks)
                    
                    # Guardar chunks en archivo de debug
                    for chunk in new_chunks:
                        f.write(f"--- CHUNK #{len(chunks) - len(new_chunks) + new_chunks.index(chunk) + 1} ---\n")
                        f.write(chunk)
                        f.write(f"\n\nTamaño: {len(chunk)} caracteres\n")
                        f.write("\n\n" + "=" * 50 + "\n\n")
                else:
                    # Procesar DataFrames sin PacienteID
                    new_chunks = self._process_df_without_patient_id(df, csv_name)

                    # Verificar y dividir chunks que exceden el límite de caracteres
                    processed_chunks = self._enforce_chunk_size_limit(new_chunks)

                    chunks.extend(new_chunks)
                    
                    # Guardar chunks en archivo de debug
                    for chunk in new_chunks:
                        f.write(f"--- CHUNK #{len(chunks) - len(new_chunks) + new_chunks.index(chunk) + 1} ---\n")
                        f.write(chunk)
                        f.write(f"\n\nTamaño: {len(chunk)} caracteres\n")
                        f.write("\n\n" + "=" * 50 + "\n\n")
            
            print(f"Se crearon {len(chunks)} chunks optimizados")
            return chunks
    
    def _enforce_chunk_size_limit(self, chunks, max_chars=cfg.MAX_CHAR_EMBEDDING, max_tokens=cfg.MAX_TOKEN_EMBEDDING):
        """
        Asegura que todos los chunks estén por debajo de los límites de caracteres y tokens.
        
        Args:
            chunks (list): Lista de chunks a procesar
            max_chars (int): Tamaño máximo en caracteres (por defecto: MAX_CHAR_EMBEDDING)
            max_tokens (int): Número máximo de tokens (por defecto: MAX_TOKEN_EMBEDDING)
            
        Returns:
            list: Lista de chunks, divididos si es necesario
        """
        result = []
        char_splits = 0
        token_splits = 0
        
        def estimate_tokens(text):
            # Estimación aproximada: ~4 caracteres por token en inglés/español
            # Esta es una estimación simple, los tokenizadores reales son más complejos
            return len(text) // 4
        
        for chunk in chunks:
            # Si el chunk está dentro de ambos límites, agregarlo directamente
            if len(chunk) <= max_chars and estimate_tokens(chunk) <= max_tokens:
                result.append(chunk)
                continue
            
            # Si excede algún límite, dividirlo
            remaining = chunk
            while len(remaining) > max_chars or estimate_tokens(remaining) > max_tokens:
                # Determinar el límite más restrictivo (caracteres o tokens)
                char_limit = max_chars
                token_limit_in_chars = max_tokens * 4  # Convertir límite de tokens a caracteres estimados
                
                effective_limit = min(char_limit, token_limit_in_chars)
                
                # Encontrar el último espacio antes del límite para dividir correctamente
                split_point = remaining.rfind(" ", 0, effective_limit)
                if split_point == -1:  # Si no hay espacios, cortar en el límite
                    split_point = effective_limit
                
                # Agregar la primera parte al resultado
                first_part = remaining[:split_point].strip()
                result.append(first_part)
                
                # Registrar qué tipo de límite causó la división
                if len(remaining) > max_chars:
                    char_splits += 1
                if estimate_tokens(remaining) > max_tokens:
                    token_splits += 1
                
                # Continuar con el resto
                remaining = remaining[split_point:].strip()
            
            # Agregar la última parte si queda algo
            if remaining:
                result.append(remaining)
        
        # Registrar si hubo divisiones
        total_splits = len(result) - len(chunks)
        if total_splits > 0:
            print(f"Se dividieron chunks: {total_splits} total, {char_splits} por caracteres, {token_splits} por tokens")
            
        return result
    
    def _build_patient_name_map(self, dataframe_list):
        """
        Builds a mapping of PacienteIDs to patient names from all DataFrames.
        
        Args:
            dataframe_list (list): List of DataFrames to scan
            
        Returns:
            dict: A mapping of {PacienteID: Nombre del Paciente}
        """
        paciente_nombre_map = {}
        
        for df in dataframe_list:
            # Buscar columna de ID de paciente
            id_column = None
            for col_name in ['PacienteID', 'pacienteid', 'PACIENTEID', 'Paciente_ID', 'ID_Paciente']:
                if col_name in df.columns:
                    id_column = col_name
                    break
            
            if not id_column:
                continue
            
            # Buscar columna de nombre de paciente
            nombre_column = None
            for col_name in ['Nombre', 'nombre', 'Name', 'name']:
                if col_name in df.columns:
                    nombre_column = col_name
                    break
            
            if not nombre_column:
                continue
                
            # Agregar nombres al mapa
            for _, row in df.iterrows():
                paciente_id = row[id_column]
                nombre = row[nombre_column]
                if pd.notna(nombre) and str(nombre).strip():  # Verificar que el nombre no sea vacío o NaN
                    paciente_nombre_map[str(paciente_id)] = str(nombre)
        
        print(f"Mapa de pacientes creado con {len(paciente_nombre_map)} entradas")
        return paciente_nombre_map

    def _process_df_with_patient_id(self, df, csv_name, paciente_nombre_map):
        """
        Process a DataFrame that contains PacienteID column.
        
        Args:
            df (DataFrame): DataFrame to process
            csv_name (str): Name of the CSV file
            paciente_nombre_map (dict): Mapping of patient IDs to names
            
        Returns:
            list: List of generated chunks
        """
        chunks = []
        
        # Determinar el nombre exacto de la columna PacienteID
        id_column = next(col for col in df.columns if col.lower() == 'pacienteid' or col == 'Paciente_ID' or col == 'ID_Paciente')
        
        # Agrupar por PacienteID
        for paciente_id, group in df.groupby(id_column):
            # Buscar el nombre del paciente en el mapa global
            nombre_paciente = paciente_nombre_map.get(str(paciente_id), "") # Devuelve "" si no lo encuentra, que se traduce como false
            
            # Si no está en el mapa, intentar obtenerlo del grupo actual
            if not nombre_paciente:
                for nombre_col in ['Nombre', 'nombre', 'Name', 'name']:
                    if nombre_col in group.columns:
                        potential_name = group[nombre_col].iloc[0] if not group.empty else ""
                        if pd.notna(potential_name) and str(potential_name).strip():
                            nombre_paciente = str(potential_name)
                            break
            
            # Crear un chunk para todo el grupo (paciente)
            patient_data = []
            
            # Agregar información del paciente, excluyendo PacienteID que ya lo incluimos en el encabezado
            for _, row in group.iterrows():
                row_data = []
                for col in group.columns:
                    # Excluir source_file, ID y nombre del paciente para evitar repetición
                    if col != 'source_file' and col != id_column and col not in ['Nombre', 'nombre', 'Name', 'name']:
                        if pd.notna(row[col]):  # Solo incluir valores que no sean NA/null
                                value = str(row[col])
                                row_data.append(f"{col}:{value}")
                
                patient_data.append(" ".join(row_data))
            
            # Unir toda la información del paciente
            all_patient_data = " | ".join(patient_data)
            
            # Crear el chunk final
            if nombre_paciente:
                chunk = f"{csv_name} -> PacienteID:{paciente_id} (Nombre:{nombre_paciente}) -> {all_patient_data}"
            else:
                chunk = f"{csv_name} -> PacienteID:{paciente_id} -> {all_patient_data}"
            
            chunks.append(chunk)
        
        return chunks

    def _process_df_without_patient_id(self, df, csv_name):
        """
        Process a DataFrame that doesn't contain PacienteID column.
        
        Args:
            df (DataFrame): DataFrame to process
            csv_name (str): Name of the CSV file
            
        Returns:
            list: List of generated chunks
        """
        chunks = []
        
        # Procesar cada fila como un chunk individual
        for idx, row in df.iterrows():
            campo_valor_pairs = []
            
            for col in df.columns:
                if col != 'source_file':
                    if pd.notna(row[col]):  # Solo incluir valores que no sean NA/null
                        value = str(row[col])
                        campo_valor_pairs.append(f"{col}:{value}")
            
            # Combinar en formato Campo:Valor
            formatted_data = " ".join(campo_valor_pairs)
            
            # Crear chunk
            chunk = f"{csv_name} -> {formatted_data}"
            chunks.append(chunk)
        
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
                    print(f"Error en solicitud a API de embeddings: {response.status_code} - {response.text} - {text}")
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
    
    def get_relevant_context(self, query, top_k=6):
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
            relevant_context += f"--- {self.text_chunks[idx]} "
        
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
        print(f"{MAGENTA}RAG:{RESET} {GREEN}{relevant_context}{RESET}")
        
        # Incluir mensajes recientes del historial (límite para ahorrar tokens)
        recent_messages = self.conversation_history[-self.max_context_messages:] if len(self.conversation_history) > self.max_context_messages else self.conversation_history
        
        # Crear lista final de mensajes
        messages = [system_message] + recent_messages
        
        return messages