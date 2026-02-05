from typing import Literal
from pydantic import BaseModel

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

product_json_data = product.model_dump_json()
print(product_json_data)

new_product = Product.model_validate_json(product_json_data)
print(new_product)
