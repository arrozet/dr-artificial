import os
import sys

# Agrega la ruta del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

from flask import Flask
from config.config import Config  # Ahora debería encontrar el módulo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrar Blueprints (rutas)
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
