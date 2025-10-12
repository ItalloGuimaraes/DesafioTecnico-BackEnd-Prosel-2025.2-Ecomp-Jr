import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.db import get_db
from model.database import Base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:itallo1230@localhost:5432/ecomp_jr_api_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    yield db
    db.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    from main import app

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # ATUALIZAÇÃO: Adicionado para depurar e ver as rotas carregadas
    print("Rotas carregadas:", [route.path for route in app.routes])
    
    yield TestClient(app)
    del app.dependency_overrides[get_db]
    
@pytest.fixture(scope="function")
def empresa_de_teste(db_session, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_data = {
        "name": "Empresa Fixture Teste",
        "cnpj": "12345678000100",
        "cidade": "Fixture City",
        "ramo_atuacao": "Fixture Ramo",
        "telefone": "11122233344",
        "email_contato": "fixture@teste.com"
    }
    
    # Usando o TestClient para criar a empresa via API
    with TestClient(app) as client:
        # Sobrescreve o get_db para esta chamada específica
        def override_get_db():
            yield db_session
        app.dependency_overrides[get_db] = override_get_db
        
        response = client.post("/empresas", headers=headers, json=empresa_data)
        assert response.status_code == 200
        
        del app.dependency_overrides[get_db]
        
    return response.json()
