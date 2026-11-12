"""Fixtures compartidas por toda la suite."""
import pytest

from api.client import ApiClient


@pytest.fixture(scope="session")
def api():
    """Cliente HTTP único para toda la sesión de pruebas."""
    client = ApiClient()
    yield client
    client.close()


@pytest.fixture
def new_post_payload():
    """Datos válidos para crear una publicación."""
    return {
        "title": "Reporte de calidad del sprint",
        "body": "Resumen de casos ejecutados y defectos encontrados.",
        "userId": 1,
    }
