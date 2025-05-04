from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: float
    description: str
    image_url: str

class Purchase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    timestamp: str

class Cart(BaseModel):
    user_id: int
    products: List[Product]
