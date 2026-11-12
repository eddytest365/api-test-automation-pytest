"""Publicaciones (/posts): lectura, filtros, CRUD y casos negativos."""
import allure
import pytest
from jsonschema import validate

from tests.schemas.schemas import POST, list_of

TOTAL_POSTS = 100
POSTS_PER_USER = 10


@allure.feature("Posts")
class TestReadPosts:
    @pytest.mark.smoke
    def test_list_posts_returns_all(self, api):
        """La lista completa responde 200 en JSON con las 100 publicaciones."""
        response = api.get("/posts")

        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]
        assert len(response.json()) == TOTAL_POSTS

    @pytest.mark.schema
    def test_list_posts_matches_schema(self, api):
        """Cada publicación de la lista cumple el contrato."""
        response = api.get("/posts")

        validate(instance=response.json(), schema=list_of(POST))

    @pytest.mark.smoke
    @pytest.mark.parametrize("post_id", [1, 50, 100])
    def test_get_post_by_id(self, api, post_id):
        """Consultar por id devuelve esa publicación (valores límite y medio)."""
        response = api.get(f"/posts/{post_id}")

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=POST)
        assert body["id"] == post_id

    def test_post_ids_are_unique(self, api):
        """No hay ids repetidos en la lista."""
        ids = [post["id"] for post in api.get("/posts").json()]

        assert len(ids) == len(set(ids))

    @pytest.mark.parametrize("user_id", [1, 5, 10])
    def test_filter_posts_by_user(self, api, user_id):
        """El filtro por usuario solo devuelve publicaciones de ese usuario."""
        response = api.get("/posts", params={"userId": user_id})

        assert response.status_code == 200
        posts = response.json()
        assert len(posts) == POSTS_PER_USER
        assert all(post["userId"] == user_id for post in posts)


@allure.feature("Posts")
@pytest.mark.negative
class TestPostsNegative:
    @pytest.mark.parametrize("post_id", [0, 101, 99999, "abc"])
    def test_get_nonexistent_post_returns_404(self, api, post_id):
        """Un id que no existe responde 404 con cuerpo vacío."""
        response = api.get(f"/posts/{post_id}")

        assert response.status_code == 404
        assert response.json() == {}

    def test_filter_by_unknown_user_returns_empty_list(self, api):
        """Filtrar por un usuario inexistente devuelve lista vacía, no un error."""
        response = api.get("/posts", params={"userId": 9999})

        assert response.status_code == 200
        assert response.json() == []

    def test_unknown_resource_returns_404(self, api):
        """Una ruta que no existe responde 404."""
        response = api.get("/recurso-inexistente")

        assert response.status_code == 404


@allure.feature("Posts")
@pytest.mark.crud
class TestPostsCrud:
    def test_create_post(self, api, new_post_payload):
        """Crear responde 201, devuelve los datos enviados y asigna un id nuevo."""
        response = api.post("/posts", json=new_post_payload)

        assert response.status_code == 201
        body = response.json()
        validate(instance=body, schema=POST)
        assert body["id"] == TOTAL_POSTS + 1
        for field, value in new_post_payload.items():
            assert body[field] == value

    def test_replace_post(self, api, new_post_payload):
        """PUT reemplaza la publicación completa y conserva su id."""
        response = api.put("/posts/1", json=new_post_payload)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == 1
        assert body["title"] == new_post_payload["title"]
        assert body["body"] == new_post_payload["body"]

    def test_update_post_title_only(self, api):
        """PATCH cambia solo el campo enviado y deja intacto el resto."""
        original = api.get("/posts/1").json()

        response = api.patch("/posts/1", json={"title": "Título actualizado"})

        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Título actualizado"
        assert body["body"] == original["body"]
        assert body["userId"] == original["userId"]

    def test_delete_post(self, api):
        """Borrar una publicación existente responde 200."""
        response = api.delete("/posts/1")

        assert response.status_code == 200
