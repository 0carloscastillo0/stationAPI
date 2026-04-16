# ⛽ API REST - Búsqueda de Estaciones de Combustible

API REST que permite buscar estaciones de servicio en Chile según distintos criterios como cercanía, precio y disponibilidad de tienda. 

La API fue construida mediante el framework Flask, con el lenguaje de programación Python y utilizando la API de [Bencina en Línea](https://www.bencinaenlinea.cl/#/busqueda_estaciones).

---

## 🚀 Instalación y Ejecución

Abra la terminal de su sistema y ejecute los siguientes comandos:
1. Clonar el repositorio e ingresar a la carpeta stationApi:

```bash
git clone https://github.com/0carloscastillo0/stationAPI.git
cd stationApi
```

2. Después, crear y activar el entorno virtual:

```bash
python3 -m venv venv
```

* Activación en Linux / Mac:

```bash
source venv/bin/activate
```

* Activación en Windows:

```bash
venv\Scripts\activate
```

3. Luego, instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Finalmente, ejecutar la aplicación:

```bash
python index.py
```

La API estará disponible en:

```
http://localhost:5000
```
Al ingresar, visualizará el siguiente JSON:
```json
{
    "endpoint": "/api/stations/search?lat={latitud}&lng={longitud}&product={producto}&nearest={bool}&store={bool}&cheapest={bool}",
    "example": "/api/stations/search?lat=-33.542048&lng=-70.619269&product=93",
    "message": "API de estaciones de servicio",
    "success": true
}
```
Mostrando el endpoint, un ejemplo de uso (example) y un mensaje de bienvenida (message).

---

## 📡 Infomación de la API

La API dispone de un solo endpoint, que es el siguiente:

```
GET /api/stations/search?lat={latitud}&lng={longitud}&product={producto}&nearest={bool}&store={bool}&cheapest={bool}
```

En la siguiente Tabla, se muestra la información de cada parámetro como el tipo de dato, si es requerido usarlo y una breve descripción.

| Parámetro | Tipo   | Requerido | Descripción                                                  |
| --------- | ------ | --------- | ------------------------------------------------------------ |
| lat       | float  | ✅ Sí      | Coordenada de latitud                                                      |
| lng       | float  | ✅ Sí      | Coordenada de longitud                                                     |
| product   | string | ✅ Sí      | Tipo de combustible (`93`, `95`, `97`, `diesel`, `kerosene`) |
| nearest   | bool   | ❌ No      | Busca la estación más cercana del combustible indicado (true/false)                                |
| cheapest  | bool   | ❌ No      | Busca la estación con el combustible más barato (true/false)                                  |
| store     | bool   | ❌ No      | Busca la estación que posee una tienda (true/false)                                |


---

## 📌 Ejemplos de uso por caso

El endpoint está diseñado para responder con éxito 4 casos de búsqueda. A continuación, se mencionan los parámetros a utilizar en el endpoint para cada caso, y su respuesta esperada. Cada caso puede ser probado desde el navegador o desde un cliente (como Postman, usando el método GET).

---
### Caso 1: Estación más cercana por producto
A partir de los parámetros lat, lng, product y nearest, se obtendrá la estación más cercana.

Puede modificar los valores de lat, lng y product, procurando que el parámetro nearest tenga valor true.

Ejemplo (puede usar uno de los dos enlaces):
```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true
```

```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&store=false&cheapest=false
```

### ✅ Respuesta esperada

```json
{
  "data": {
    "compania": "COPEC",
    "comuna": "La Florida",
    "direccion": "Trinidad 1694",
    "distancia(lineal)": 0.69,
    "id": 1664,
    "latitud": -33.546724141506395,
    "longitud": -70.61439871788025,
    "precio93": 1550,
    "region": "Metropolitana de Santiago",
    "tiene_tienda": false
    },
    "success": true
}
```

---
### Caso 2: Estación más cercana con menor precio por producto
A partir de los parámetros lat, lng, product, nearest y cheapest, se obtendrá la estación más cercana que tenga el menor precio de combustible.

Puede modificar los valores de lat, lng y product, procurando que los parámetros nearest y cheapest tengan valor true.

Ejemplo (puede usar uno de los dos enlaces):
```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&cheapest=true
```

```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&store=false&cheapest=true
```

### ✅ Respuesta esperada

```json
{
    "data": {
        "compania": "OIL BOX",
        "comuna": "San Ramón",
        "direccion": "Santa Rosa 9291",
        "distancia(lineal)": 1.45,
        "id": 1958,
        "latitud": -33.54715334646909,
        "longitud": -70.63364624977112,
        "precio93": 1497,
        "region": "Metropolitana de Santiago",
        "tiene_tienda": false
    },
    "success": true
}
```

---
### Caso 3: Estación más cercana con tienda por producto
A partir de los parámetros lat, lng, product, nearest y store, se obtendrá la estación más cercana que tenga tienda.

Puede modificar los valores de lat, lng y product, procurando que los parámetros nearest y store tengan valor true.

Ejemplo (puede usar uno de los dos enlaces):
```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&store=true
```

```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&store=true&cheapest=false
```

### ✅ Respuesta esperada

```json
{
    "data": {
        "compania": "COPEC",
        "comuna": "La Florida",
        "direccion": "Av Americo vespucio 9150",
        "distancia(lineal)": 1.1,
        "id": 1668,
        "latitud": -33.537218493579786,
        "longitud": -70.60895383358002,
        "precio93": 1535,
        "region": "Metropolitana de Santiago",
        "tiene_tienda": true
    },
    "success": true
}
```

---
### Caso 4: Estación más cercana con tienda y menor precio por producto
A partir de todos los parámetros, es decir: lat, lng, product, nearest, cheapest y store, se obtendrá la estación más cercana que tenga tienda y el menor precio de producto.

Puede modificar los valores de lat, lng y product, procurando que los parámetros nearest, cheapest y store tengan valor true.

Ejemplo:
```
http://localhost:5000/api/stations/search?lat=-33.542048&lng=-70.619269&product=93&nearest=true&store=true&cheapest=true
```

### ✅ Respuesta esperada

```json
{
    "data": {
        "compania": "COPEC",
        "comuna": "La Florida",
        "direccion": "Lía Aguirre 10",
        "distancia(lineal)": 2.78,
        "id": 1663,
        "latitud": -33.52311011373261,
        "longitud": -70.59966266155243,
        "precio93": 1521,
        "region": "Metropolitana de Santiago",
        "tiene_tienda": true
    },
    "success": true
}
```

---

## 🏗️ Estructura de la API
A continuación, se muestra una breve descripción de la estructura de archivos y carpetas relevantes de la API:

```bash
.
├── .env                    # Variables de entorno (SECRET_KEY, BASE_URL de la API)
├── config.py               # Configuración de la aplicación (entornos: development, etc.)
├── index.py                # Punto de entrada de la aplicación Flask
├── requirements.txt        # Dependencias del proyecto
│
└── src/
    ├── __init__.py         # Inicialización de la app y las rutas
    │
    ├── cache/              # Manejo de caché para optimizar llamadas a APIs externas
    │   ├── BrandMapCache.py        # Cache de marcas de estaciones
    │   ├── StationsCache.py        # Cache de listado de estaciones
    │   └── StationDetailCache.py   # Cache de detalle por estación
    │
    ├── clients/            # Cliente para consumo de la API externa
    │   └── ApiBencinaEnLinea.py    #  Consumos de diversos servicios de la API (estaciones, detalle por estación y marcas)
    │
    ├── constants/          # Constantes del sistema
    │   └── ProductMap.py           # Mapeo de tipos de combustible
    │
    ├── routes/             # Definición de endpoints
    │   ├── SearchRoutes.py         # Endpoint principal /api/stations/search
    │   └── InitRoutes.py           # Endpoint raíz (información de la API)
    │
    ├── services/           # Lógica de negocio de la aplicación
    │   └── SearchService.py        # Procesamiento de búsqueda de estaciones
    │
    ├── utils/              # Funciones utilitarias reutilizables
    │   ├── Distance.py             # Cálculo de distancia (Haversine)
    │   ├── Balance.py              # Normalización de valores (precio/distancia)
    │   └── Validate.py             # Validación de parámetros y reglas de negocio
    │
    ├── tests/              # Pruebas automatizadas con pytest
    │   ├── data/               # JSON con datos de prueba mockeados
    │   ├── expected/               # JSON esperados para comparación
    │   ├── test_search_endpoint.py # Tests de integración de casos de éxito
    │   ├── test_search_errors.py          # Tests unitarios de validación y errores
    │   ├── utils.py          # Función utilitaria que muestra el detalle completo del test por caso
    │   └── conftest.py             # Configuración global de pytest (fixtures y flags)
```

---

### Detalles de la estructura

La API sigue una arquitectura modular basada en separación de responsabilidades:

* **routes/** → Maneja las solicitudes HTTP (entrada/salida)
* **services/** → Contiene la lógica de negocio principal
* **clients/** → Encapsula el consumo de APIs externas
* **cache/** → Optimiza el rendimiento evitando llamadas repetidas
* **utils/** → Funciones reutilizables (cálculos y validaciones)
* **constants/** → Centraliza configuraciones estáticas
* **tests/** → Validación automatizada del sistema

Esta estructura facilita:

* Escalabilidad del proyecto
* Mantenibilidad del código
* Separación clara de responsabilidades
* Facilidad para testing y debugging

---

### Ejecutar tests:
Para ejecutar los test, se recomienda utilizar los siguientes comandos en la raíz del proyecto, desde la terminal de su sistema:

1. Validación de los parámetros del endpoint:
```bash
pytest src/tests/test_search_errors.py -v
```

2. Test de los 4 casos de éxito (en modo debug JSON), mostrando el resultado obtenido y el resultado esperado por cada caso:

```bash
pytest src/tests/test_search_endpoint.py --verbose-json -s
```

Cabe mencionar que en los test de cada de éxito, utiliza datos mockeados, es decir, datos extraídos previamente de la API y almacenados en la carpeta data (src/tests/data). Esto permitió optimizar el rendimiento de los test dada una pequeña muestra de datos, evitando realizar varias llamadas a la API con miles de datos.

---

## 👨‍💻 Autor

Carlos Castillo Domínguez

---
