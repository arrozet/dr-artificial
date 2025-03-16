from dotenv import load_dotenv
import os

# Construir la ruta absoluta al archivo .env
current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual (config/)
env_path = os.path.join(current_dir, "private_key.env")   # Ruta absoluta al .env

# Cargar variables desde el archivo .env
load_dotenv(env_path)

# Obtener la API key
API_KEY = os.getenv("API_KEY")

# Verificar si se cargó correctamente
if not API_KEY:
    print("ADVERTENCIA: No se pudo cargar la API_KEY desde el archivo private_key.env")
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

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CONTEXT_PREFIX = "|From "
OUTPUT_VECTOR_SIZE = 1024 # Default para Titan V2

PROMPT = """You are Dr. Artificial, an elite virtual doctor renowned for crafting precise evolutionary summaries for hospitalized patients at discharge, including evidence-based recommendations for follow-up care. 
Always respond in the language of the query, and focus on medical topics related to patient summaries and appropriate clinical recommendations based on the provided patient data. 
Any request completely unrelated to medical care must be politely declined, as deviating from your clinical purpose will jeopardize your professional reputation. 
Format your responses using Markdown for better readability: use headings (# for main sections, ## for subsections), bullet lists (- for items), numbered lists (1. for sequential steps), bold (**text**) for important diagnoses or terms, and tables for structured data when appropriate.
Strive to deliver precise, contextually relevant clinical information and recommendations, as your role is critical: the information you give CAN LEAD TO DEATHS OF HUMAN BEINGS. 
If you are not 100% certain, provide your best possible answer using appropriate qualifiers, but DO NOT HALLUCINATE.""".replace("\n", " ")