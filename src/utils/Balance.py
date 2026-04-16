# Clase del Balance de relevancia entre dos valores
class Balance():

    # Función para normalizar un valor entre 0 y 1
    # Entrada: valor a normalizar (value: float), valor mínimo (value:float) y valor máximo (value:float)
    # Salida: valor normalizado entre 0 y 1 (float)
    @staticmethod
    def normalize(value, min_val, max_val):
        if max_val == min_val:
            return 0  # evitar división por cero
        return (value - min_val) / (max_val - min_val)