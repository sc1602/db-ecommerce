from pydantic import BaseModel

class CreateRoleSchema(BaseModel):
    name: str

class RoleSchema(CreateRoleSchema):
    id: int
    status: bool