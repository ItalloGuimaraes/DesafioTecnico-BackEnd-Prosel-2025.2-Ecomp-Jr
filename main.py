from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from config.db import Session
from schemas.empresas import EmpresaCreate, EmpresaSchema, EmpresaUpdate
from model.empresas import Empresa
from typing import List, Optional

app = FastAPI()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Cria uma empresa
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


# Lista todas as empresas do banco de dados e aplica os filtros e busca
@app.get("/empresas", response_model=List[EmpresaSchema])
def get_empresas(
    db: Session = Depends(get_db),
    cidade: Optional[str] = None,
    ramo_atuacao: Optional[str] = None,
    nome: Optional[str] = None
):
    # Inicia a consulta base
    query = db.query(Empresa)

    # Aplica o filtro de cidade, se ele for fornecido
    if cidade:
        query = query.filter(Empresa.cidade == cidade)

    # Aplica o filtro de ramo de atuação, se ele for fornecido
    if ramo_atuacao:
        query = query.filter(Empresa.ramo_atuacao == ramo_atuacao)

    # Aplica a busca textual pelo nome, se for fornecida
    if nome:
        query = query.filter(Empresa.name.ilike(f"%{nome}%"))

    # Executa a consulta final e retorna os resultados
    return query.all()

# Exibe os detalhes de uma empresa pelo id
@app.get("/empresas/{empresa_id}")
def get_empresa_by_id(empresa_id: int, db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if (not db_empresa):
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    return db_empresa

# Atualiza os dados de uma empresa, a partir do id
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

# Deleta uma empresa do banco de dados, a partir do id
@app.delete("/empresas/{empresa_id}")
def delete_empresa(empresa_id: int ,db: Session = Depends(get_db)):
    db_empresa = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if (not db_empresa):
        raise HTTPException(status_code=404, detail="Empresa não encontrada!")
    
    db.delete(db_empresa)
    db.commit()
    return {"detail": "Empresa deletada com sucesso!"}