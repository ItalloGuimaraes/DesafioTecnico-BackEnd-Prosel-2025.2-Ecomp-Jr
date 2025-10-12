from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Defina suas credenciais aqui ---
username = "postgres"
password = "itallo1230"
host = "localhost"
port = 5432
database = "ecomp_jr_api"

# --- Crie la string de conexão (URL DSN) manualmente ---
DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# --- Crie o engine usando a string de conexão ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# --- ATUALIZAÇÃO: Adicionar a função get_db ---
def get_db():
    """
    Função 'dependency' que cria e fornece uma sessão de banco de dados por requisição.
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()