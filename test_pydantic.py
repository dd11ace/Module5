from venv import logger
from pydantic import BaseModel
import jsonschema


class User2(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True


user2_data = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": True,
}


def test_jsonschema():
    # Валидируем данные с использованием JSON Schema
    try:
        user_schema = User2.model_json_schema()
        jsonschema.validate(user2_data, user_schema)
        logger.info("Данные валидны!")
    except jsonschema.ValidationError as e:
        logger.info("Ошибка валидации:", e)
