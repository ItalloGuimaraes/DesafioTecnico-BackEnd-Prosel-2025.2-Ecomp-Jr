from pydantic import BaseModel
from typing import Optional

# Schema para a criação de um novo administrador
class AdminCreate(BaseModel):
    username: str
    password: str

# Schema para a resposta de um administrador (sem a senha)
class AdminSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Schema para a resposta do token de login
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema de dados embutido no token JWT
class TokenData(BaseModel):
    username: Optional[str] = None