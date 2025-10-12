from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from config.db import Session
from schemas.empresas import EmpresaCreate, EmpresaSchema, EmpresaUpdate
from model.empresas import Empresa
from typing import List

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Cria a empresa
@app.post("/empresas", response_model=EmpresaSchema)
def create_empresa(empresa: EmpresaCreate, db: Session = Depends(get_db)):
    try:
        nova_empresa = Empresa(**empresa.model_dump())
        db.add(nova_empresa)
        db.commit()
        db.refresh(nova_empresa)
        return nova_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma empresa com este CNPJ ou e-mail.")



@app.get("/empresas")
def get_empresas(db: Session = Depends(get_db)):
    return db.query(Empresa).all()



@app.get("/empresas/{empresa_id}")
def get_empresa_by_id(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if (not db_empresa):
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    return db_empresa


@app.put("/empresas/{empresa_id}")
def update_empresa(empresa_id: int, empresa_data: EmpresaUpdate ,db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if (not db_empresa):
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    
    for (key, value) in empresa_data.model_dump().items():
        setattr(db_empresa, key, value)
        
    db.commit()
    db.refresh(db_empresa)
    return db_empresa


@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int ,db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if (not db_empresa):
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    
    db.delete(db_empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso"}