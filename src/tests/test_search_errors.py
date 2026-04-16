# Importaciones
import pytest
from src import init_app
from config import config
from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea


# Función para iniciar la app para el test
@pytest.fixture
def client():
    app = init_app(config["development"])
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# -----------------------------
# VALIDACIÓN DE ERRORES
# -----------------------------

# Función que verifique los parámetros obligatorios faltantes
def test_missing_required_params(client):
    response = client.get("/api/stations/search")

    result = response.get_json()

    assert response.status_code == 400
    assert result["success"] == False
    assert "lat" in result["error"]


# Función que verifique un producto inválido
def test_invalid_product(client):
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.45,
            "lng": -70.66,
            "product": "94"
        }
    )

    result = response.get_json()

    assert response.status_code == 400
    assert result["success"] == False
    assert "product" in result["error"]


# Función que verifique el formato de lat y lng inválidos
def test_invalid_lat_lng(client):
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": "abc",
            "lng": "xyz",
            "product": "93"
        }
    )

    result = response.get_json()

    assert response.status_code == 400
    assert result["success"] == False
    assert "lat" in result["error"]


# Función que verifique el formato inválido de los parámetros opcionales (nearest en este caso)
def test_invalid_boolean_param(client):
    response = client.get(
        "/api/stations/search",
        query_string={
            "lat": -33.45,
            "lng": -70.66,
            "product": "93",
            "nearest": "invalid"
        }
    )

    result = response.get_json()

    # comportamiento actual: no falla
    assert response.status_code == 400
    assert result["success"] == False
    assert "nearest" in result["error"]


# Función que verifique el endpoint base (debe dar un objeto con el dato del endpoint)
def test_root_endpoint(client):
    response = client.get("/")

    result = response.get_json()

    assert response.status_code == 200
    assert result["success"] == True
    assert "endpoint" in result
