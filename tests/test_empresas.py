import pytest
from fastapi.testclient import TestClient

# Fixtures de Preparação

@pytest.fixture(scope="function")
def auth_token(client: TestClient):
    client.post("/admins/register", json={"username": "testuser", "password": "testpassword"})
    
    response = client.post(
        "/admins/login", 
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200, f"Falha no login: {response.json()}"
    token_data = response.json()
    return token_data["access_token"]

@pytest.fixture(scope="function")
def empresa_criada(client: TestClient, auth_token: str):
    # Cria uma empresa no banco de dados e retorna seus dados
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_data = {
        "name": "Empresa de Teste Padrão",
        "cnpj": "11111111000111",
        "cidade": "Cidade Teste",
        "ramo_atuacao": "Testes",
        "telefone": "11999999999",
        "email_contato": "padrão@teste.com"
    }
    response = client.post("/empresas", headers=headers, json=empresa_data)
    assert response.status_code == 200
    return response.json()

# Testes da API

# Testa a rota raiz
def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à API de Gerenciamento de Empresas!"}
    
# Testa a criação de uma nova empresa 
def test_create_empresa(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_data = {
        "name": "Empresa Criada no Teste",
        "cnpj": "22222222000122",
        "cidade": "Cidade Nova",
        "ramo_atuacao": "Criação",
        "telefone": "22999999999",
        "email_contato": "criacao@teste.com"
    }
    response = client.post("/empresas", headers=headers, json=empresa_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == empresa_data["name"]
    assert "id" in data
    

# Testa a listagem de empresas, garantindo que a empresa criada existe na lista
def test_get_empresas(client: TestClient, auth_token: str, empresa_criada: dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/empresas", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Verifica se o ID da empresa criada na fixture está na lista de IDs retornados
    ids_na_lista = [empresa["id"] for empresa in data]
    assert empresa_criada["id"] in ids_na_lista
    
# Testa a busca de uma empresa pelo seu ID dinâmico
def test_get_empresa_by_id(client: TestClient, auth_token: str, empresa_criada: dict):
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_id = empresa_criada["id"] # Usa o ID real da empresa criada para este teste
    response = client.get(f"/empresas/{empresa_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == empresa_id
    assert data["name"] == empresa_criada["name"]
    
# Testa a busca por um ID que não existe
def test_get_empresa_by_id_not_found(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/empresas/99999", headers=headers)
    assert response.status_code == 404

# Testa a atualização de uma empresa usando seu ID dinâmico
def test_update_empresa(client: TestClient, auth_token: str, empresa_criada: dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_id = empresa_criada["id"]
    update_data = {"cidade": "Cidade Atualizada"}
    response = client.put(f"/empresas/{empresa_id}", headers=headers, json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["cidade"] == "Cidade Atualizada"

# Testa a exclusão de uma empresa
def test_delete_empresa(client: TestClient, auth_token: str): 
    headers = {"Authorization": f"Bearer {auth_token}"}
    empresa_para_deletar = {
        "name": "Empresa a Deletar",
        "cnpj": "99888777000166",
        "cidade": "Cidade a Deletar",
        "ramo_atuacao": "Exclusão",
        "telefone": "11111111111",
        "email_contato": "deletar@teste.com"
    }
    create_response = client.post("/empresas", headers=headers, json=empresa_para_deletar)
    
    # Verificação para garantir que a criação foi bem-sucedida
    assert create_response.status_code == 200, f"Falha ao criar empresa para deletar: {create_response.json()}"
    new_id = create_response.json()["id"]

    # Deleta a empresa recém-criada
    delete_response = client.delete(f"/empresas/{new_id}", headers=headers)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Empresa deletada com sucesso!"}

    # Tenta buscar a empresa deletada para confirmar que não existe mais
    get_response = client.get(f"/empresas/{new_id}", headers=headers)
    assert get_response.status_code == 404

# Testa a rota de listagem com filtros
def test_get_empresas_with_filters(client: TestClient, auth_token: str, empresa_criada: dict):
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    cidade = empresa_criada["cidade"]
    response = client.get(f"/empresas?cidade={cidade}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for empresa in data:
        assert empresa["cidade"] == cidade

    response_vazio = client.get("/empresas?cidade=CidadeInexistente", headers=headers)
    assert response_vazio.status_code == 200
    assert response_vazio.json() == []