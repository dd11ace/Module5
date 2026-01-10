from venv import logger
from pydantic import BaseModel, Field
import jsonschema
from enum import Enum


"""
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class ProductType(str, Enum):
    NEW = "new"
    PREVIOUS_USE = "previous_use"


class Manufacturer(BaseModel):
    name: str
    city: Optional[str] = None
    street: Optional[str] = None


class Product(BaseModel):
    # поле name может иметь длину в диапазоне от 3 до 50 символов
    name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
    # поле price должно быть больше 0
    price: float = Field(..., gt=0, description="Цена продукта")
    # поле in_stock принимает булево значение и установится по умолчанию = False
    in_stock: bool = Field(default=False, description="Есть ли в наличии")
    # поле color должно быть строкой и принимает значение "black" по умолчанию
    color: str = "black"
    # поле year не обязательное. Можно не указывать при создании объекта
    year: Optional[int] = None
    # поле product принимает тип Enum (может содержать только 1 из его значений)
    product: ProductType
    # поле manufacturer принимает тип другой BaseModel
    manufacturer: Manufacturer


def test_product():
    # Пример создания объекта + в поле price передаем строку вместо числа
    product = Product(
        name="Laptop",
        price="999.99",
        product=ProductType.NEW,
        manufacturer=Manufacturer(name="MSI"),
    )
    logger.info(f"{product}")

    # Пример конвертации объекта в JSON
    json_data = product.model_dump_json(exclude_unset=True)
    logger.info(f"{json_data}")

    # Пример конвертации JSON в объект
    new_product = Product.model_validate_json(json_data)
    logger.info(f"{new_product}")
"""

"""
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from venv import logger


class PostgresClient:
    # Mock - заглушка вместо реального сервиса
    @staticmethod
    def get(key: str) -> None:
        return None


class Card(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16, description="Номер карты")
    cvc: str = Field(..., min_length=3, max_length=3)

    @field_validator("pan")  # кастомный валидатор для проверки поля pan
    def check_pan(cls, value: str) -> str:
        # Проверяем, существует ли карта в Redis
        if PostgresClient.get(f"card_by_pan_{value}") is None:
            raise ValueError("Такойкарты не существует")
        return value


def test_field_validator():
    try:
        card = Card(pan="1111222233334444", cvc="123")
        logger.info(card)
    except ValidationError as e:
        logger.info(f"Ошибка валидации: {e}")
        raise
"""
"""
from pydantic import BaseModel, Field, model_validator
from enum import Enum


class CardType(str, Enum):
    VISA = "Visa"
    AMEX = "American Express"


class Card(BaseModel):
    pan: str = Field(..., min_length=16, max_length=16)
    cvc: str = Field(..., min_length=3, max_length=4)
    card_type: CardType

#     @model_validator(mode="before")
#     def check_cvc_for_card_type(cls, values: list):
#         """
#         Проверяем, что:
#         - У карт VISA cvc == 3 цифры
#         - У карт AMEX cvc == 4 цифры
#         """
#         if values["card_type"] == CardType.VISA and len(values["cvc"]) != 3:
#             raise ValueError("CVC для VISA должен быть 3 цифры")
#         if values["card_type"] == CardType.AMEX and len(values["cvc"]) != 4:
#             raise ValueError("CVC для AMEX должен быть 4 цифры")
#         return values


# def test_cards():
#     Card(pan="1234567890123456", cvc="123", card_type=CardType.VISA)  #  Всё ок
#     # Card(
#     #     pan="1234567890123456", cvc="1234", card_type=CardType.VISA
#     # )  #  Ошибка: CVC для VISA должен быть 3 цифры
#     Card(pan="1234567890123456", cvc="1234", card_type=CardType.AMEX)  #  Всё ок
#     logger.info(Card)


# class User2(BaseModel):
#     id: int
#     name: str
#     email: str
#     is_active: bool = True


# def test_model_json_schema():
#     user_schema = User2.model_json_schema()
#     logger.info(user_schema)


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
