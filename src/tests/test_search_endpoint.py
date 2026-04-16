# Importaciones
import json
import pytest

from src import init_app
from config import config
from src.tests.utils import print_json_comparison

# Función para iniciar la app para el test
@pytest.fixture
def client():
    app = init_app(config["development"])
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Función que carga el resultado esperado en JSON (para cada caso correspondiente)
def load_expected(filename):
    with open(f"src/tests/expected/{filename}", encoding="utf-8") as f:
        return json.load(f)


# Función Helper para mostrar el detalle completo de cada test
def assert_and_debug(test_name, expected, result, verbose_json):
    success_ok = result["success"] == True
    data_ok = result["data"] == expected
    passed = success_ok and data_ok

    if verbose_json:
        print_json_comparison(test_name, expected, result["data"], passed)

    assert success_ok
    assert data_ok


# -----------------------------
# Caso 1: Estación más cercana
# -----------------------------
# Función test que encuentre la estación más cercana a la ubicación dada
def test1_nearest_station(client, verbose_json):
    # Se obtiene la respuesta real y la esperada
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.542048,
            "lng": -70.619269,
            "product": "93",
            "nearest": "true"
        }
    )
    result = response.get_json()
    expected = load_expected("one_nearest.json")

    # Assertion real
    assert response.status_code == 200

    # Debug opcional
    assert_and_debug(
        "test1_nearest_station",
        expected,
        result,
        verbose_json
    )


# -----------------------------------------
# Caso 2: Más cercana + menor precio
# -----------------------------------------
# Función test que encuentre la estación más cercana que tenga el menor precio de combustible
def test2_cheapest_nearest_station(client, verbose_json):
    # Se obtiene la respuesta real y la esperada
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.542048,
            "lng": -70.619269,
            "product": "93",
            "nearest": "true",
            "cheapest": "true"
        }
    )
    result = response.get_json()
    expected = load_expected("two_cheapest.json")

    # Assertion real
    assert response.status_code == 200

    # Debug opcional
    assert_and_debug(
        "test2_cheapest_nearest_station",
        expected,
        result,
        verbose_json
    )


# -----------------------------------------
# Caso 3: Más cercana con tienda
# -----------------------------------------
# Función test que encuentre la estación más cercana que tenga tienda
def test3_store_station(client, verbose_json):
    # Se obtiene la respuesta real y la esperada
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.542048,
            "lng": -70.619269,
            "product": "93",
            "nearest": "true",
            "store": "true"
        }
    )
    result = response.get_json()
    expected = load_expected("three_store.json")

    # Assertion real
    assert response.status_code == 200

    # Debug opcional
    assert_and_debug(
        "test3_store_station",
        expected,
        result,
        verbose_json
    )


# ------------------------------------------------
# Caso 4: Más cercana + tienda + menor precio
# ------------------------------------------------
# Función test que encuentre la estación maś cercana que tenga tienda y el menor precio
def test4_store_cheapest_station(client, verbose_json):
    # Se obtiene la respuesta real y la esperada
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.542048,
            "lng": -70.619269,
            "product": "93",
            "nearest": "true",
            "store": "true",
            "cheapest": "true"
        }
    )
    result = response.get_json()
    expected = load_expected("four_store_cheapest.json")

    # Assertion real
    assert response.status_code == 200

    # Debug opcional
    assert_and_debug(
        "test4_store_cheapest_station",
        expected,
        result,
        verbose_json
    )