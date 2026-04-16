from src.constants.ProductMap import PRODUCT_MAP

# Clase que valida ciertos criterios
class Validate():

    # Función para validar si una estación de servicio tiene "tienda de conveniencia"
    # Entrada: Detalle de la estación de servicio (JSON)
    # Salida: True si tiene tienda de conveniencia, False si no (bool)
    @staticmethod
    def has_store_detail(station_detail):
        if not station_detail:
            return False

        data = station_detail.get("data", {})

        for service in data.get("servicios", []):
            name = (service.get("nombre") or "").lower()

            if "tienda de conveniencia" in name:
                return True

        return False
    

    # Función para validar los parámetros de entrada del endpoint de la API
    # Entrada: argumentos de entrada (lat:float, lng:float, product:string)
    # Salida: Retorno de parámetros validados (lat:float, lng:float, product:string, nearest:bool, cheapest:bool, store:bool) o mensaje de error
    @staticmethod
    def validate_search_params(args):
        lat = args.get("lat")
        lng = args.get("lng")
        product = args.get("product")

        if not lat or not lng or not product:
            raise ValueError(
                "Ingrese los parámetros requeridos: lat, lng y product"
            )

        try:
            lat = float(lat)
            lng = float(lng)
        except ValueError:
            raise ValueError(f"Los parámetros lat y lng deben ser números válidos (lat:-33.123456, lng:-70.123456). Valores recibidos: lat:{lat}, lng:{lng}")
        
        if not PRODUCT_MAP.get(product.lower()):
            raise ValueError(f"El parámetro product debe ser 93, 95, 97, diesel o kerosene. Valor recibido: '{product}'")

        nearest = Validate.parse_bool(args.get("nearest"), "nearest")
        cheapest = Validate.parse_bool(args.get("cheapest"), "cheapest")
        store = Validate.parse_bool(args.get("store"), "store")

        return lat, lng, product, nearest, cheapest, store
    

    # Función que convierte un string a boolean, validando valores permitidos.
    # Entrada: value (string), field_name (string)
    # Salida: Valor booleano (boolean) o mensaje de error
    @staticmethod
    def parse_bool(value, field_name):
        """
        Convierte un string a boolean validando valores permitidos.
        """
        if value is None:
            return False  # valor por defecto

        value_lower = value.lower()

        if value_lower == "true":
            return True
        elif value_lower == "false":
            return False
        else:
            raise ValueError(
                f"El parámetro '{field_name}' debe ser 'true' o 'false'. Valor recibido: '{value}'"
            )
        
        
