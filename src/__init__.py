# Importaciones
from flask import Flask

from .routes import SearchRoutes
from .routes import InitRoutes


# Función que inicia la app
# Entrada: Configuración de la app
# Salida: Aplicación iniciada
def init_app(config):
    # Invocar Flask
    app = Flask(__name__)
    
    # Configuración de la app
    app.config.from_object(config)

    # Blueprints
    app.register_blueprint(InitRoutes.main)
    app.register_blueprint(SearchRoutes.main, url_prefix="/api/stations/search")

    return app
