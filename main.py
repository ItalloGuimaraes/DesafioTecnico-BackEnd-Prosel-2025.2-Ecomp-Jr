from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from config.db import engine
from model.database import Base
import model.empresas
import model.admins

Base.metadata.create_all(bind=engine)

from config.db import get_db, Session
from schemas.empresas import EmpresaCreate, EmpresaSchema, EmpresaUpdate
from schemas.admins import AdminSchema
from model.empresas import Empresa
from auth import get_current_admin
from routers import admins

# Criação e Configuração do App 
app = FastAPI()
app.include_router(admins.router)


# Definição das Rotas

# Cria uma empresa (protegida)
@app.post("/empresas", response_model=EmpresaSchema)
def create_empresa(
    empresa: EmpresaCreate, 
    db: Session = Depends(get_db),
    current_admin: AdminSchema = Depends(get_current_admin) # ROTA PROTEGIDA
):
    try:
        nova_empresa = Empresa(**empresa.model_dump())
        db.add(nova_empresa)
        db.commit()
        db.refresh(nova_empresa)
        return nova_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma empresa com este CNPJ ou e-mail.")

# Lista todas as empresas (protegida)
@app.get("/empresas", response_model=List[EmpresaSchema])
def get_empresas(
    db: Session = Depends(get_db),
    cidade: Optional[str] = None,
    ramo_atuacao: Optional[str] = None,
    nome: Optional[str] = None,
    current_admin: AdminSchema = Depends(get_current_admin) # ROTA PROTEGIDA
):
    query = db.query(Empresa)
    if cidade:
        query = query.filter(Empresa.cidade == cidade)
    if ramo_atuacao:
        query = query.filter(Empresa.ramo_atuacao == ramo_atuacao)
    if nome:
        query = query.filter(Empresa.name.ilike(f"%{nome}%"))
    return query.all()

# Exibe os detalhes de uma empresa pelo id (protegida)
@app.get("/empresas/{empresa_id}", response_model=EmpresaSchema)
def get_empresa_by_id(
    empresa_id: int, 
    db: Session = Depends(get_db),
    current_admin: AdminSchema = Depends(get_current_admin) # ROTA PROTEGIDA
):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    return db_empresa

# Atualiza os dados de uma empresa (protegida)
@app.put("/empresas/{empresa_id}", response_model=EmpresaSchema)
def update_empresa(
    empresa_id: int, 
    empresa_data: EmpresaUpdate, 
    db: Session = Depends(get_db),
    current_admin: AdminSchema = Depends(get_current_admin) # ROTA PROTEGIDA
):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    
    for key, value in empresa_data.model_dump(exclude_unset=True).items(): 
        setattr(db_empresa, key, value)
    
    try:
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma empresa com este CNPJ ou e-mail.")

# Deleta uma empresa (protegida)
@app.delete("/empresas/{empresa_id}")
def delete_empresa(
    empresa_id: int, 
    db: Session = Depends(get_db),
    current_admin: AdminSchema = Depends(get_current_admin) # ROTA PROTEGIDA
):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not db_empresa:
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    
    db.delete(db_empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso!"}

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Gerenciamento de Empresas!"}