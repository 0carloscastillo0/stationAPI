# Importaciones
import requests
from decouple import config

# Clase para consumir la API BencinaEnLinea
class ApiBencinaEnLinea():

    # API client de bencina en Línea
    BASE_URL = config("BASE_URL")

    # Función para obtener estaciones de servicio
    # Entrada: ---
    # Salida: Todas las estaciónes de servicio (response.json()) o None
    @staticmethod
    def get_stations():
        try:
            url = f"{ApiBencinaEnLinea.BASE_URL}/busqueda_estacion_filtro"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener las estaciones de servicio: {e}")
            return None


    # Función para obtener detalle de una estación de servicio por ID
    # Entrada: ID de la estación (int)
    # Salida: Detalle de la estación de servicio (repsonse.json()) o None
    @staticmethod
    def get_station_detail(station_id):
        try:
            response = requests.get(f"{ApiBencinaEnLinea.BASE_URL}/estacion_ciudadano/{station_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error obteniendo detalle estación {station_id}: {e}")
            return None


    # Función para obtener todas las marcas de estaciones de servicio
    # Entrada: ---
    # Salida: Lista de todas las marcas (response.json()) o None
    @staticmethod
    def get_brands():
        try:
            url = f"{ApiBencinaEnLinea.BASE_URL}/marca_ciudadano"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error al obtener todas las marcas: {e}")
            return None