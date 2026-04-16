# Importaciones
import pytest
import json
from src.clients.ApiBencinaEnLinea import ApiBencinaEnLinea
from src.cache.BrandMapCache import BrandMapCache

# Función que parsee el resultado del test en consola, mediante un diseño personalizado
def pytest_addoption(parser):
    parser.addoption(
        "--verbose-json",
        action="store_true",
        default=False,
        help="Mostrar comparación detallada de JSON en cada test"
    )


# Función que retorne el comando opcional para expandir el resultado de cada test
@pytest.fixture
def verbose_json(request):
    return request.config.getoption("--verbose-json")


# Función que obtiene el path para cargar los datos dentro de la carpeta "data"
def load_json(path):
    with open(path) as f:
        return json.load(f)

# -----------------------------
# MOCK API FIXTURE
# -----------------------------
# Función mock que Mockea todas las llamadas externas:
#
# get_stations
# get_stations_detail
# get_brands
#
# Usando los datos locales desde src/tests/data/
@pytest.fixture(autouse=True)
def mock_api(monkeypatch):
    # Obtención de datos locales
    stations_data = load_json("src/tests/data/stations.json")
    details_data = load_json("src/tests/data/station_details.json")
    brands_data = load_json("src/tests/data/brands.json")

    # MOCK: get_stations, obteniendo todas las estaciones (en este caso, de la comuna de "La Florida" y "San Ramón").
    def mock_get_stations():
        return {"data": stations_data}

    # MOCK: get_station_detail, obteniendo el detalle completo de las estaciones de "La Florida" y "San Ramón".
    def mock_get_station_detail(station_id):
        return details_data.get(str(station_id), {})

    # MOCK: get_brands, obteniendo todas las marcas 
    def mock_get_brands():
        return {"data": brands_data}

    # Aplicar monkeypatch
    monkeypatch.setattr(ApiBencinaEnLinea, "get_stations", mock_get_stations)
    monkeypatch.setattr(ApiBencinaEnLinea, "get_station_detail", mock_get_station_detail)
    monkeypatch.setattr(ApiBencinaEnLinea, "get_brands", mock_get_brands)

    # Resetear cache para evitar contaminación entre tests
    BrandMapCache._cache = None

    yield