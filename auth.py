from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

# Importe os modelos e schemas necessários
import model.admins
import schemas.admins
from config.db import get_db

# Configuração de Segurança
SECRET_KEY = "sua_chave_secreta_super_dificil"  # Lembre-se de trocar por uma chave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funções de Senha ---

def verify_password(plain_password, hashed_password):
    """Verifica se a senha em texto puro corresponde à senha com hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Gera o hash de uma senha em texto puro."""
    return pwd_context.hash(password)

# --- Funções de Token JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um novo token de acesso (JWT)."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Define um tempo de expiração padrão se nenhum for passado
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependência de Autenticação ---

# CORREÇÃO: Definição do oauth2_scheme ANTES da função que o utiliza
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_admin(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    """
    Dependência que extrai o token, valida e retorna o usuário admin logado.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.admins.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    admin = db.query(model.admins.Admin).filter(model.admins.Admin.username == token_data.username).first()
    if admin is None:
        raise credentials_exception
        
    return admin