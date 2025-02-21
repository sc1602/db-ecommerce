from pydantic import BaseModel

class CreateCategorySchema(BaseModel):
    name: str

class CategorySchema(CreateCategorySchema):
    id: int
    status: bool
    created_at: str
    updated_at: str