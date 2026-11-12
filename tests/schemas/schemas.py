"""JSON Schemas de las respuestas. Definen el contrato esperado de cada recurso."""

POST = {
    "type": "object",
    "required": ["userId", "id", "title", "body"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
}

COMMENT = {
    "type": "object",
    "required": ["postId", "id", "name", "email", "body"],
    "properties": {
        "postId": {"type": "integer"},
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "body": {"type": "string"},
    },
}

USER = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string", "minLength": 1},
        "username": {"type": "string", "minLength": 1},
        "email": {"type": "string", "pattern": r"^[^@\s]+@[^@\s]+\.[^@\s]+$"},
        "address": {
            "type": "object",
            "required": ["street", "city", "zipcode", "geo"],
            "properties": {
                "geo": {
                    "type": "object",
                    "required": ["lat", "lng"],
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"},
                    },
                },
            },
        },
        "company": {
            "type": "object",
            "required": ["name"],
            "properties": {"name": {"type": "string"}},
        },
    },
}

TODO = {
    "type": "object",
    "required": ["userId", "id", "title", "completed"],
    "properties": {
        "userId": {"type": "integer"},
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "completed": {"type": "boolean"},
    },
}


def list_of(item_schema: dict) -> dict:
    """Schema de una lista cuyos elementos cumplen `item_schema`."""
    return {"type": "array", "items": item_schema}
