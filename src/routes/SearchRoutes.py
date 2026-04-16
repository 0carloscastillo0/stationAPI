# Importaciones
from flask import request, jsonify, Blueprint

from src.services.SearchService import SearchService

from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea

from src.utils.Validate import Validate

from src.cache.BrandMapCache import BrandMapCache

from src.constants.ProductMap import PRODUCT_MAP


main = Blueprint("search_blueprint",__name__)

# Función que define la ruta para la búsqueda de estaciones de servicio según cada parámetro de entrada
# Entrada: Payload (requeridos: lat(float), lng(float), product(string). Opcionales: nearest(bool), cheapest(bool), store(bool))
# Salida: Estación encontrada (JSON) o mensaje de error (JSON).
@main.route("")
def search_station():
    try:
        # Validación de los parámetros de entrada y del producto
        lat, lng, product, nearest, cheapest, store = Validate.validate_search_params(request.args)
        
        # Llamar a la función de búsqueda de estaciones con los parámetros proporcionados
        result = SearchService.search_stations(lat, lng, product, nearest, cheapest, store)

        # Obtener la información resultante de la estación
        station = result["station"]

        # Obtener el precio del producto, incluyendo el tipo de producto
        product_code = PRODUCT_MAP.get(product.lower())
        price_key = f"precio{product_code}"

        # Obtener si la estación posee la tienda o no
        detail = ApiBencinaEnLinea.get_station_detail(station["id"])
        tiene_tienda = Validate.has_store_detail(detail)

        # Obtener el nombre de la marca (compania)
        brands_map = BrandMapCache.get()
        marca_id = station.get("marca")
        compania = brands_map.get(marca_id, "Desconocida")

        # Retorna el JSON con todos los datos incluídos
        return jsonify({
            "success": True,
            "data": {
                "id": station["id"],
                "compania": compania,
                "direccion": station["direccion"],
                "comuna": station["comuna"],
                "region": station["region"],
                "latitud": float(station["latitud"]),
                "longitud": float(station["longitud"]),
                "distancia(lineal)": round(result["distance"], 2),
                price_key: result["price"],
                "tiene_tienda": tiene_tienda
            }
        })

    # Manejo de errores
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Error interno del servidor"
        }), 500
