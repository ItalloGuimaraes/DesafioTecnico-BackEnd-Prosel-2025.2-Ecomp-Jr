from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from config.db import engine
from datetime import datetime

Base = declarative_base()

class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column("nome", String(255))
    cnpj = Column(String(255), unique=True, index=True)
    cidade = Column(String(255))
    ramo_atuacao = Column(String(255))
    telefone = Column(String(255))
    email_contato = Column(String(255), unique=True, index=True)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)