# Importaciones
from src.cache.StationDetailCache import StationDetailCache
from src.cache.StationCache import StationCache

from src.utils.Distance import Distance
from src.utils.Balance import Balance
from src.utils.Validate import Validate

# Clase conteniendo el servicio principal de búsqueda
class SearchService():
    
    # Función principal para buscar estaciones de servicio según criterios
    # Entrada: latitud (lat: float), longitud (lng: float), producto (product: float), (nearest: bool, cheapest: bool, store: bool)
    # Salida: Estación de servicio (JSON) o mensaje de error (JSON).
    @staticmethod
    def search_stations(lat, lng, product, nearest=False, cheapest=False, store=False):

        # Obtener lista de estaciones desde el cliente de la API
        stations = StationCache.get()["data"]

        # Construir dataset base
        candidates = []
        for station in stations:
            # Calcular la distancia entregada y de la estación usando la fórmula de Haversine
            try:
                distance = Distance.haversine(
                    lat,
                    lng,
                    float(station["latitud"]),
                    float(station["longitud"])
                )
            except:
                continue

            # Verificar si la estación tiene el producto solicitado y su precio
            for fuel in station.get("combustibles", []):
                if fuel["nombre_corto"] == product and fuel["precio"]:
                    try:
                        price = int(float(fuel["precio"]))

                        candidates.append({
                            "station": station,
                            "price": price,
                            "distance": distance
                        })

                    except:
                        continue

        # Si no hay candidatos, retornar None
        if not candidates:
            return None
        
        #--------
        # CASOS
        #--------
        # Caso 1 de estación más cercana por producto (nearest)
        if nearest:
            candidates.sort(key=lambda x: x["distance"])
        
        # Caso 3 de estación más cercana con tienda por producto (store + nearest)
        if store:
            # Obtener estaciones que poseen tiendas (primeras 10 más cercanas)
            filtered = []
            count = 0
            for item in candidates:
                if count >= 10:
                    break

                try:
                    station_id = item["station"]["id"]
                    detail = StationDetailCache.get(station_id)
                except:
                    continue

                if Validate.has_store_detail(detail):
                    filtered.append(item)
                    count += 1

            # Si no quedan candidatos, retornar None
            if not filtered:
                return None
            
            candidates = filtered

        # Caso 2 de estación más cercana con menor precio por producto (cheapest + nearest)
        if cheapest:
            # Obtener las primeras 5 estaciones más cercanas
            subset = candidates[:5]

            # Obtener precios y distancias (max y min en ambos casos)
            prices = [x["price"] for x in subset]
            distances = [x["distance"] for x in subset]
            min_price, max_price = min(prices), max(prices)
            min_dist, max_dist = min(distances), max(distances)

            # Puntaje para priorizar tanto el precio barato como la distancia entre estaciones.
            W_PRICE = 0.8
            W_DISTANCE = 0.2

            # Ordenar por la métrica combinada mediante normalización
            subset.sort(
                key=lambda x: (
                    W_PRICE * Balance.normalize(x["price"], min_price, max_price) +
                    W_DISTANCE * Balance.normalize(x["distance"], min_dist, max_dist)
                )
            )

            candidates = subset

        # Nota: El Caso 4, combina el Caso 1, el Caso 2 y el Caso 3 (nearest + store + cheapest)

        # Retornar el primer candidato de estación
        return candidates[0]