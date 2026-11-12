"""Usuarios (/users) y sus tareas (/todos)."""
import allure
import pytest
from jsonschema import validate

from tests.schemas.schemas import TODO, USER, list_of

TOTAL_USERS = 10


@allure.feature("Users")
class TestUsers:
    @pytest.mark.smoke
    @pytest.mark.schema
    def test_list_users_matches_schema(self, api):
        """Los 10 usuarios cumplen el contrato, incluidos los objetos anidados."""
        response = api.get("/users")

        assert response.status_code == 200
        users = response.json()
        assert len(users) == TOTAL_USERS
        validate(instance=users, schema=list_of(USER))

    def test_usernames_and_emails_are_unique(self, api):
        """No hay dos usuarios con el mismo username ni el mismo email."""
        users = api.get("/users").json()

        assert len({user["username"] for user in users}) == TOTAL_USERS
        assert len({user["email"].lower() for user in users}) == TOTAL_USERS

    def test_get_user_by_id(self, api):
        """Consultar un usuario por id devuelve ese usuario."""
        response = api.get("/users/1")

        assert response.status_code == 200
        body = response.json()
        validate(instance=body, schema=USER)
        assert body["id"] == 1

    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [0, 11])
    def test_get_nonexistent_user_returns_404(self, api, user_id):
        """Los ids justo fuera del rango válido (1-10) responden 404."""
        response = api.get(f"/users/{user_id}")

        assert response.status_code == 404


@allure.feature("Todos")
class TestTodos:
    @pytest.mark.schema
    def test_todos_of_user_match_schema(self, api):
        """Las tareas de un usuario cumplen el contrato y le pertenecen."""
        response = api.get("/users/1/todos")

        assert response.status_code == 200
        todos = response.json()
        assert todos, "se esperaba al menos una tarea"
        validate(instance=todos, schema=list_of(TODO))
        assert all(todo["userId"] == 1 for todo in todos)

    @pytest.mark.parametrize("completed", [True, False])
    def test_filter_todos_by_status(self, api, completed):
        """El filtro por estado solo devuelve tareas en ese estado."""
        response = api.get("/todos", params={"completed": str(completed).lower()})

        assert response.status_code == 200
        todos = response.json()
        assert todos, "se esperaba al menos una tarea"
        assert all(todo["completed"] is completed for todo in todos)
