# Importaciones
from flask import jsonify, Blueprint

main = Blueprint("init_blueprint",__name__)

# Función que define la ruta de inicio
# Entrada: ---
# Salida: Mensaje de inicio (JSON)
@main.route("/")
def root_info():
    return jsonify({
        "success": True,
        "message": "API de estaciones de servicio",
        "endpoint": "/api/stations/search?lat={latitud}&lng={longitud}&product={producto}&nearest={bool}&store={bool}&cheapest={bool}",
        "example": "/api/stations/search?lat=-33.542048&lng=-70.619269&product=93"
    })