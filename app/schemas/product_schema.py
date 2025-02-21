from pydantic import BaseModel

class CreateProductSchema(BaseModel):
    name: str
    description: str
    brand: str
    size: str
    price: float
    stock: int
    category_id: int

class ProductSchema(CreateProductSchema):
    id: int
    code: str
    image: str
    status: bool
    created_at: str
    updated_at: str

class SaleProductSchema(BaseModel):
    id: int
    code: str
    name: str