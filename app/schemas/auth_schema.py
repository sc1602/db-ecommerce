from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str
    role_id: int

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    status: bool
    created_at: str
    updated_at: str
    role_id: int