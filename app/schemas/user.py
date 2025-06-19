from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    sobrenome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    senha_hash: str = Field(..., min_length=6, max_length=128)

class UserResponse(BaseModel):
    nome: str
    sobrenome: str
    email: EmailStr

class UserUpdate(BaseModel):
    nome: str = Field(None, min_length=2, max_length=100)
    sobrenome: str = Field(None, min_length=2, max_length=100)
    email: EmailStr = None