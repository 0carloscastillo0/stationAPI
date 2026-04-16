# Importaciones
from config import config
from src import init_app

# Cargar configuración en la App
configuration = config["development"]
app = init_app(configuration)

# Iniciar aplicación Flask
if __name__ == "__main__":
    app.run()