from pydantic import BaseModel
from typing import Optional

class ProductIn(BaseModel):
    name: str
    price: float
    stock: int
    description: Optional[str] = None

class ProductOut(ProductIn):
    id: int

class OrderIn(BaseModel):
    product_id: int
    quantity: int
