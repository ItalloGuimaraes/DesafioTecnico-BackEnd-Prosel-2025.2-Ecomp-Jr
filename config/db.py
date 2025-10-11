from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- Defina suas credenciais aqui ---
username = "postgres"
password = "itallo1230"
host = "localhost"
port = 5432
database = "ecomp_jr_api"

# --- Crie a string de conexão (URL DSN) manualmente ---
DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# --- Crie o engine usando a string de conexão ---
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)