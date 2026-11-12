# API Test Automation — Python + pytest

[![API tests](https://github.com/eddytest365/api-test-automation-pytest/actions/workflows/tests.yml/badge.svg)](https://github.com/eddytest365/api-test-automation-pytest/actions/workflows/tests.yml)

Suite de pruebas automatizadas para una API REST, construida con Python y pytest. Usa [JSONPlaceholder](https://jsonplaceholder.typicode.com) como API pública de práctica, así cualquiera puede clonar el repo y ejecutarla sin credenciales.

El objetivo es mostrar cómo estructuro una suite de API: cliente HTTP reutilizable, validación de contrato con JSON Schema, casos negativos, datos parametrizados e integración continua.

## Qué cubre

| Área | Qué se verifica |
|---|---|
| **Lectura** | Códigos de estado, tipo de contenido, cantidad de registros, ids únicos |
| **Filtros** | Resultados por usuario, por publicación y por estado |
| **CRUD** | Crear (201), reemplazar con PUT, actualizar con PATCH y borrar |
| **Negativos** | Ids inexistentes y valores límite (404), filtros sin resultados, rutas desconocidas |
| **Contrato** | Estructura y tipos de cada recurso contra su JSON Schema, incluidos objetos anidados y formato de email |
| **Consistencia** | La ruta anidada y el filtro equivalente devuelven lo mismo |

32 pruebas sobre 4 recursos: `posts`, `comments`, `users` y `todos`.

## Stack

Python 3.12 · pytest · requests · jsonschema · Allure · GitHub Actions

## Estructura

```
├── api/
│   ├── client.py          # Cliente HTTP: URL base, timeout y reintentos
│   └── config.py          # Configuración por variables de entorno
├── tests/
│   ├── conftest.py        # Fixtures compartidas
│   ├── schemas/           # JSON Schemas (contrato de cada recurso)
│   ├── test_posts.py
│   ├── test_comments.py
│   └── test_users.py
├── .github/workflows/     # Pipeline de integración continua
└── pytest.ini             # Marcadores y opciones
```

## Cómo ejecutarla

```bash
git clone https://github.com/eddytest365/api-test-automation-pytest.git
cd api-test-automation-pytest
python -m venv .venv
.venv/Scripts/activate          # en Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Por tipo de prueba:

```bash
pytest -m smoke        # verificación rápida
pytest -m crud         # creación, actualización y borrado
pytest -m negative     # casos negativos
pytest -m schema       # validación de contrato
```

Reporte de Allure (requiere [Allure CLI](https://allurereport.org/docs/install/)):

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

Para apuntar a otro entorno, copia `.env.example` como `.env` y cambia `API_BASE_URL`.

## Integración continua

Cada push a `main` y cada pull request ejecuta la suite completa en GitHub Actions y guarda los resultados de Allure como artefacto de la ejecución.

## Decisiones de diseño

- **Los tests no conocen la URL ni el timeout.** Todo pasa por `ApiClient`, así cambiar de entorno es cambiar una variable.
- **Los schemas viven aparte de los tests.** Si el contrato cambia, se actualiza en un solo lugar.
- **Reintentos solo en lecturas.** Un fallo transitorio de red no debe marcar un test como fallido, pero una escritura nunca se repite sola.
- **Marcadores estrictos.** Un marcador mal escrito rompe la ejecución en lugar de ignorarse.

## Autor

**Eddy Sáenz** — QA Engineer · [GitHub](https://github.com/eddytest365) · [LinkedIn](https://linkedin.com/in/eddy-saenz-021200al)
