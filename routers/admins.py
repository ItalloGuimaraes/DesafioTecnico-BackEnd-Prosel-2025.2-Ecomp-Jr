from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Importações dos outros módulos do projeto
from schemas.admins import AdminCreate, AdminSchema, Token
from model.admins import Admin
from auth import get_password_hash, verify_password, create_access_token
from config.db import get_db
from datetime import timedelta

router = APIRouter(
    # O prefixo foi removido para que a rota de login seja /login
    # As tags agrupam as rotas na documentação automática
    tags=["Auth"] 
)

@router.post("/register", response_model=AdminSchema)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        username=admin.username, 
        hashed_password=hashed_password
    )
    db.add(db_admin)
    try:
        db.commit()
        db.refresh(db_admin)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username já cadastrado."
        )
    return db_admin

# --- ADICIONE ESTA NOVA ROTA ---
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Busca o admin no banco pelo username
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()

    # 2. Verifica se o admin existe e se a senha está correta
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Define o tempo de expiração do token
    access_token_expires = timedelta(minutes=30)
    
    # 4. Cria o token de acesso JWT
    access_token = create_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    
    # 5. Retorna o token
    return {"access_token": access_token, "token_type": "bearer"}