"""Comentarios: recurso anidado en /posts/{id}/comments y filtro en /comments."""
import allure
import pytest
from jsonschema import validate

from tests.schemas.schemas import COMMENT, list_of

COMMENTS_PER_POST = 5


@allure.feature("Comments")
class TestComments:
    @pytest.mark.smoke
    @pytest.mark.schema
    def test_comments_of_post_match_schema(self, api):
        """Los comentarios de una publicación cumplen el contrato (incluye formato de email)."""
        response = api.get("/posts/1/comments")

        assert response.status_code == 200
        validate(instance=response.json(), schema=list_of(COMMENT))

    @pytest.mark.parametrize("post_id", [1, 100])
    def test_comments_belong_to_requested_post(self, api, post_id):
        """Solo se devuelven comentarios de la publicación pedida."""
        comments = api.get(f"/posts/{post_id}/comments").json()

        assert len(comments) == COMMENTS_PER_POST
        assert all(comment["postId"] == post_id for comment in comments)

    def test_nested_route_and_filter_return_same_comments(self, api):
        """La ruta anidada y el filtro por postId son dos caminos al mismo resultado."""
        nested = api.get("/posts/2/comments").json()
        filtered = api.get("/comments", params={"postId": 2}).json()

        assert nested == filtered

    @pytest.mark.negative
    def test_comments_of_nonexistent_post_is_empty(self, api):
        """Una publicación inexistente no tiene comentarios."""
        response = api.get("/comments", params={"postId": 9999})

        assert response.status_code == 200
        assert response.json() == []
