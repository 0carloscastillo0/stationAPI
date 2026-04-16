# Importaciones
import time
from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea

# Clase indicando una caché para guardar las marcas de estaciones
class BrandMapCache():
    _cache = None
    _cache_time = 0
    _ttl = 3600  # segundos (1 hora)

    # Función para guardar y obtener los datos de las marcas en la caché
    # Entrada: --
    # Salida: _cache (dict)
    @staticmethod
    def get():
        current_time = time.time()

        # Si no hay cache o expiró
        if BrandMapCache._cache is None or (current_time - BrandMapCache._cache_time) > BrandMapCache._ttl:
            data = ApiBencinaEnLinea.get_brands()["data"]

            # Crear diccionario: {id: nombre}
            BrandMapCache._cache = {
                brand["id"]: brand["nombre"]
                for brand in data
            }

            # Guardar momento de actualización
            BrandMapCache._cache_time = current_time

        return BrandMapCache._cache