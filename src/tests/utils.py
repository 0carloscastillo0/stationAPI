# Importaciones
from colorama import Fore, Style
import json

# Función que muestre el detalle completo de cada resultado del test
# Entrada: Nombre del test (test_name: string), resultado esperado (expected: JSON), resultado actual (actual: JSON), flag (passed: string)
# Salida: ---
def print_json_comparison(test_name, expected, actual, passed):
    color = Fore.GREEN if passed else Fore.RED

    print("\n" + "="*60)
    print(f"{color}TEST: {test_name}{Style.RESET_ALL}")
    print("-"*60)

    print("EXPECTED:")
    print(json.dumps(expected, indent=2, ensure_ascii=False))

    print("\nACTUAL:")
    print(json.dumps(actual, indent=2, ensure_ascii=False))

    print("-"*60)
    print(f"{color}RESULT: {'PASSED' if passed else 'FAILED'}{Style.RESET_ALL}")
    print("="*60 + "\n")