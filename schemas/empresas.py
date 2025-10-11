from pydantic import BaseModel
from datetime import datetime

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
        from_attributes = True # Permite que o Pydantic leia dados de objetos SQLAlchemy
    