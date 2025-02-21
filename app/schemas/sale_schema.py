from pydantic import BaseModel, EmailStr

class CreateCustomerSchema(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    address: str
    document_number: str

class CreateSaleDetailSchema(BaseModel):
    quantity: int
    price: float
    subtotal: float
    product_id: int

class CreateSaleSchema(BaseModel):
    total: float
    customer: CreateCustomerSchema
    details: list[CreateSaleDetailSchema]

class CustomerSchema(BaseModel):
    id: int
    name: str
    last_name: str
    email: EmailStr
    address: str
    document_number: str

class SaleSchema(BaseModel):
    id: int
    code: str
    total: float
    status: str
    created_at: str
    updated_at: str

class SaleDetailSchema(BaseModel):
    id: int
    quantity: int
    price: float
    subtotal: float