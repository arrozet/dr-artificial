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