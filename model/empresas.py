from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
from .database import Base

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column("nome", String(255))
    cnpj = Column(String(255), unique=True, index=True)
    cidade = Column(String(255))
    ramo_atuacao = Column(String(255))
    telefone = Column(String(255))
    email_contato = Column(String(255), unique=True, index=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(UTC))
