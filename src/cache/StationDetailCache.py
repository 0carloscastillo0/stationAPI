# Importaciones
import time
from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea

# Clase indicando una caché para guardar el detalle de una estación
class StationDetailCache:
    _cache = {}
    _ttl = 300  # 5 minutos

    # Función para guardar y obtener el detalle de una estación desde la caché
    # Entrada: --
    # Salida: data (desde el cached)
    @staticmethod
    def get(station_id):
        current_time = time.time()

        # Revisar cache
        cached = StationDetailCache._cache.get(station_id)

        if cached:
            data, timestamp = cached

            # Si no ha expirado
            if (current_time - timestamp) < StationDetailCache._ttl:
                return data

        # Si no existe o expiró → llamar API
        data = ApiBencinaEnLinea.get_station_detail(station_id)

        # Guardar en cache
        StationDetailCache._cache[station_id] = (data, current_time)

        return data

    @staticmethod
    def clear():
        StationDetailCache._cache = {}