# Importación
from decouple import config

# Clase que usa la llave secreta en el archivo .env
class Config():
    SECRET_KEY = config("SECRET_KEY")

# Clase que inicia la app en modo DEBUG
class DevelopmentConfig(Config):
    DEBUG = True

config = {
    "development": DevelopmentConfig
}