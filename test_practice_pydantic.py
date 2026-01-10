from enum import Enum
from typing import Literal
from pydantic import BaseModel


# class ProductType(Enum):
#     CLOTHES = "Одежда"
#     ELECTRONICS = "Электроника"

product_type = Literal[
    "Одежда",
    "Электроника",
]


class Product(BaseModel):
    name: str
    product_type: product_type
    price: float
    in_stock: bool = False


product = Product(
    name="Ноутбук", product_type="Электроника", price=150000, in_stock="false"
)

# Сериализация (Python --> JSON)
product_json_data = product.model_dump_json()
print(product_json_data)

# Десериализация (JSON --> Python)
new_product = Product.model_validate_json(product_json_data)
print(new_product)
