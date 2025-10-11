from fastapi import FastAPI
from config.db import Session
from schemas.empresas import EmpresaCreate, EmpresaSchema
from model.empresas import Empresa

app = FastAPI()

@app.get("/")
def get_info():
    return {"Hello": "World!"}

@app.post("/empresas", response_model=EmpresaSchema)
def create_empresa(empresa: EmpresaCreate): 
    with Session() as session:
        nova_empresa = Empresa(**empresa.model_dump())
        session.add(nova_empresa)
        session.commit()
        session.refresh(nova_empresa)
        
        return nova_empresa

