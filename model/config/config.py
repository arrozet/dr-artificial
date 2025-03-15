from dotenv import load_dotenv
import os

# Configuración de modelos y sus identificadores
# El modelo seleccionado será el que use la aplicación

# Modelo activo (cambiar este valor para usar otro modelo)
ACTIVE_MODEL = "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"

# Lista de modelos disponibles para usar
AVAILABLE_MODELS = {
    "claude-3-5-sonnet": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
    "claude-3-opus": "bedrock/anthropic.claude-3-opus-20240229-v1:0",
    "claude-3-haiku": "bedrock/anthropic.claude-3-haiku-20240307-v1:0",
    "gpt-4": "openai/gpt-4",
    "gpt-3.5-turbo": "openai/gpt-3.5-turbo"
}

CSV_PATH = "./data/"
CONTEXT_PREFIX = "|From "
OUTPUT_VECTOR_SIZE = 1024 # Default para Titan V2
PROMPT = """You are Dr. Artificial, an elite virtual doctor renowned for crafting precise evolutionary summaries for hospitalized patients at discharge, including evidence-based recommendations for follow-up care. 
Always respond in the language of the query, and focus on medical topics related to patient summaries and appropriate clinical recommendations based on the provided patient data. Any request completely unrelated to medical care must be politely declined, as deviating from your clinical purpose will jeopardize your professional reputation. 
Strive to deliver precise, contextually relevant clinical information and recommendations, as your role is critical: the information you give CAN LEAD TO DEATHS OF HUMAN BEINGS. 
If you are not 100% certain, provide your best possible answer using appropriate qualifiers, but DO NOT HALLUCINATE.""".replace("\n", " ")

# Cargar el archivo .env
load_dotenv("./config/private_key.env")

# Obtener la API key
API_KEY  = os.getenv("API_KEY")