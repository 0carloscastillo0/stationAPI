# Importaciones
import time
from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea

# Clase indicando una caché para guardar todas las estaciones disponibles
class StationCache:
    _cache = None
    _cache_time = 0
    _ttl = 300  # 5 minutos

    # Función para guardar y obtener las estaciones en la caché
    # Entrada: --
    # Salida: _cache (el data)
    @staticmethod
    def get():
        current_time = time.time()

        # Si no hay cache o expiró
        if (
            StationCache._cache is None or
            (current_time - StationCache._cache_time) > StationCache._ttl
        ):
            data = ApiBencinaEnLinea.get_stations()

            # Guardar datos completos (incluye "data")
            StationCache._cache = data
            StationCache._cache_time = current_time

        return StationCache._cache

    @staticmethod
    def clear():
        StationCache._cache = None
        StationCache._cache_time = 0