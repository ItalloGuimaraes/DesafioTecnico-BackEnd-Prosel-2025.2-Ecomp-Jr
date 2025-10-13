# DesafioTecnico-BackEnd-Prosel-2025.2-Ecomp-Jr
````markdown
# API de Gerenciamento de Empresas Clientes - Prosel Ecomp Jr. 2025.2

## 📝 Descrição

Esta API foi desenvolvida como solução para o Desafio Técnico da trilha Back-End da Ecomp Jr. O objetivo é criar o núcleo de um sistema centralizado para gerenciar informações de empresas clientes, resolvendo os desafios de dados descentralizados em planilhas e garantindo consistência para futuras aplicações.

A API implementa funcionalidades completas de CRUD (Create, Read, Update, Delete) para as empresas, consultas avançadas com filtros e busca, e um sistema de autenticação e segurança baseado em tokens JWT para proteger os dados, conforme os requisitos do desafio.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework Principal:** FastAPI
* **Banco de Dados:** PostgreSQL
* [cite_start]**ORM:** SQLAlchemy (para a comunicação entre a aplicação e o banco de dados) 
* **Validação de Dados:** Pydantic
* [cite_start]**Autenticação:** JWT (JSON Web Tokens) com as bibliotecas `python-jose` e `passlib[bcrypt]` 
* [cite_start]**Testes Automatizados:** Pytest (para testes de integração dos endpoints)
* **Servidor ASGI:** Uvicorn

## 📋 Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados em sua máquina:
* Python 3.10 ou superior.
* PostgreSQL.
* Git.
* Um cliente de API, como o Postman ou Insomnia.

## 🚀 Guia de Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em um ambiente local.

### 1. Clonar o Repositório
git clone [https://github.com/ItalloGuimaraes/DesafioTecnico-BackEnd-Prosel-2025.2-Ecomp-Jr.git](https://github.com/ItalloGuimaraes/DesafioTecnico-BackEnd-Prosel-2025.2-Ecomp-Jr.git)
cd DesafioTecnico-BackEnd-Prosel-2025.2-Ecomp-Jr
````

### 2\. Configurar o Ambiente Virtual

É altamente recomendado utilizar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente no Windows
.venv\Scripts\Activate.ps1

# Ative o ambiente no Linux/Mac
source .venv/bin/activate
```

### 3\. Instalar as Dependências

Este projeto utiliza um arquivo `requirements.txt` para gerenciar as dependências. Se ele não existir, gere-o com o comando `pip freeze > requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Configurar o Banco de Dados

  - Verifique se o seu servidor PostgreSQL está em execução.
  - Crie um banco de dados para a aplicação. Exemplo: `CREATE DATABASE ecomp_jr_api;`.
  - Ajuste a string de conexão `DATABASE_URL` no arquivo principal (`main.py` ou `config/db.py`) com suas credenciais de acesso (usuário, senha, nome do banco).

### 5\. Executar a Aplicação

Com o ambiente ativado e o banco configurado, inicie o servidor da API:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`. A documentação interativa gerada pelo FastAPI pode ser acessada em `http://127.0.0.1:8000/docs`.

### 6\. Executar os Testes Automatizados

Para garantir a confiabilidade da API, execute a suíte de testes automatizados com o `pytest`. Certifique-se de ter um banco de dados de teste separado e configurado no arquivo `tests/conftest.py`.

```bash
pytest
```

## 📚 Referência da API

As rotas de CRUD e consulta de empresas são protegidas e exigem um token de autenticação JWT.

-----

### Autenticação

#### `POST /register`

  * **Descrição:** Registra um novo administrador no sistema.
  * **Postman:** `POST /admins/register'
  * **Corpo da Requisição (`application/json`):**
    ```json
    {
      "username": "admin_user",
      "password": "admin_password"
    }
    ```
  * **Resposta de Sucesso (`200 OK`):** Retorna o `id` e `username` do administrador criado.

#### `POST /login`

  * **Descrição:** Autentica um administrador e retorna um token de acesso JWT.
  * **Postman:** `POST /admins/login'
  * **Corpo da Requisição (`x-www-form-urlencoded`):**
      * `username`: admin\_user
      * `password`: admin\_password
  * **Resposta de Sucesso (`200 OK`):**
    ```json
    {
      "access_token": "seu_token_jwt",
      "token_type": "bearer"
    }
    ```

-----

### Gerenciamento de Empresas

#### `POST /empresas`

  * **Descrição:** Cadastra uma nova empresa cliente.
  * **Autenticação:** Obrigatória.
  * **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
  * **Corpo da Requisição (`application/json`):**
    ```json
    {
      "name": "Tech Inovações SA",
      "cnpj": "12345678000199",
      "cidade": "Feira de Santana",
      "ramo_atuacao": "Tecnologia",
      "telefone": "75999998888",
      "email_contato": "contato@techinovacoes.com"
    }
    ```
  * **Resposta de Erro (`409 Conflict`):** Se o `cnpj` ou `email_contato` já estiverem cadastrados.

#### `GET /empresas`
* **Descrição:** Lista todas as empresas cadastradas. Suporta filtros opcionais por `cidade` e `ramo_atuacao`, e busca textual por `nome`.
* **Autenticação:** Obrigatória.
* **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
* **Parâmetros de Consulta (Opcionais):**
    * `cidade` (string): Filtra as empresas pela cidade informada. Ex: `?cidade=Salvador`
    * `ramo_atuacao` (string): Filtra as empresas pelo ramo de atuação. Ex: `?ramo_atuacao=Tecnologia`
    * `nome` (string): Realiza uma busca textual e retorna empresas que contenham o texto no nome. Ex: `?nome=Tech`
* **Exemplo de Uso Combinado:** `GET /empresas?cidade=Salvador&nome=Inova`
* **Resposta de Sucesso (`200 OK`):** Retorna uma lista `[]` de objetos de empresa. Se nenhum filtro for aplicado, retorna todas as empresas. Se os filtros não encontrarem resultados, retorna uma lista vazia.

#### `GET /empresas/{empresa_id}`

  * **Descrição:** Retorna os detalhes de uma única empresa pelo seu ID.
  * **Autenticação:** Obrigatória.
  * **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
  * **Resposta de Erro (`404 Not Found`):** Se a empresa com o ID especificado não for encontrada.

#### `PUT /empresas/{empresa_id}`

  * **Descrição:** Atualiza os dados de uma empresa existente (exceto `id`, `cnpj` e `data_de_cadastro`).
  * **Autenticação:** Obrigatória.
  * **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
  * **Corpo da Requisição (`application/json`):** Apenas os campos a serem atualizados.
    ```json
    {
      "cidade": "São Paulo",
      "telefone": "11988887777"
    }
    ```

#### `PUT /empresas/{empresa_id}`
* **Descrição:** Atualiza os dados de uma empresa existente (exceto `id`, `cnpj` e `data_de_cadastro`).
* **Autenticação:** Obrigatória.
* **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
* **Corpo da Requisição (`application/json`):** Apenas os campos a serem atualizados.
    ```json
    {
      "cidade": "São Paulo",
      "telefone": "11988887777"
    }
    ```
* **Resposta de Sucesso (`200 OK`):** Retorna o objeto da empresa com os dados atualizados.
* **Resposta de Erro (`404 Not Found`):** Se a empresa com o ID especificado não for encontrada.

#### `DELETE /empresas/{empresa_id}`

  * **Descrição:** Exclui uma empresa do banco de dados.
  * **Autenticação:** Obrigatória.
  * **Teste pelo Postman:** Passos: Authorization -> Auth Type -> Bearer Token -> Cola o conteudo de "access_token" do login.
  * **Resposta de Sucesso (`200 OK`):**
    ```json
    {
      "detail": "Empresa deletada com sucesso!"
    }
    ```

<!-- end list -->

---

## 👨‍💻 Autor

Desenvolvido por **Ítallo Guimarães**.

* **GitHub:** [ItalloGuimaraes](https://github.com/ItalloGuimaraes)
* **LinkedIn:** [Ítallo Guimarães](www.linkedin.com/in/ítallo-guimarães-782832274)
