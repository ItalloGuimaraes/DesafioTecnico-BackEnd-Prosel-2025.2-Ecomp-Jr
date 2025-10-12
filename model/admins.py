from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base 
from config.db import engine

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))


Base.metadata.create_all(bind=engine)