from pydantic import BaseModel, EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserRegister(UserAuth):
    nome: str = Field(..., min_length=2, max_length=100)
    sobrenome: str = Field(..., min_length=2, max_length=100)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: EmailStr | None = None
