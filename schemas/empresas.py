from pydantic import BaseModel
from datetime import datetime
from typing import Optional 

class EmpresaCreate(BaseModel):
    name: str
    cnpj: str
    cidade: str
    ramo_atuacao: str
    telefone: str
    email_contato: str

# Herda os campos de EmpresaCreate e adiciona os que são gerados pelo banco
class EmpresaSchema(EmpresaCreate):
    id: int 
    data_cadastro: datetime
    
    class Config:
        from_attributes = True 

# Campos opcionais
class EmpresaUpdate(BaseModel):
    name: Optional[str] = None
    cidade: Optional[str] = None
    ramo_atuacao: Optional[str] = None
    telefone: Optional[str] = None
    email_contato: Optional[str] = None