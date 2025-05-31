from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr

class UserCreate(UserBase):
    senha_hash: str

class UserResponse(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr

class UserUpdate(BaseModel):
    nome: str = None
    sobrenome: str = None
    email: EmailStr = None