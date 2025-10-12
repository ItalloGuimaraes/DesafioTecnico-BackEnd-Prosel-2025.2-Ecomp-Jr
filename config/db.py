from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


username = "postgres"
password = "itallo1230"
host = "localhost"
port = 5432
database = "ecomp_jr_api"

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()