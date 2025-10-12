from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base # Importando o Base de um modelo já existente
from config.db import engine

Base = declarative_base()

# Verifique se o nome da classe é exatamente "Admin"
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))

# Garante que a tabela seja criada no banco, se não existir
Base.metadata.create_all(bind=engine)