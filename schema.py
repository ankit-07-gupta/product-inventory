from pydantic import BaseModel


class Product(BaseModel):
    id: int
    product: str
    category: str
    price: float

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str
    category: str
    price: float

