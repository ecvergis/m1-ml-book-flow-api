# BookFlow API

API pública desenvolvida como projeto da Pós Tech em Machine Learning da FIAP. Fornece dados de livros processados para sistemas de recomendação e análise, integrando etapas de extração, transformação e disponibilização. Projetada com foco em escalabilidade, modularidade e reuso em modelos de aprendizado de máquina.

## 📋 Índice

- [Descrição do Projeto e Arquitetura](#-descrição-do-projeto-e-arquitetura)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Instruções para Execução](#-instruções-para-execução)
- [Documentação das Rotas da API](#-documentação-das-rotas-da-api)
- [Exemplos de Chamadas](#-exemplos-de-chamadas)
- [Boas Práticas Utilizadas](#-boas-práticas-utilizadas)

---

## 🏗️ Descrição do Projeto e Arquitetura

### Descrição

O BookFlow API é uma API REST desenvolvida em Python com FastAPI que fornece:

- **Gerenciamento de Livros**: CRUD completo para livros com busca avançada
- **Estatísticas**: Análises e métricas sobre os livros cadastrados
- **Web Scraping**: Coleta automática de dados de livros de sites externos
- **Autenticação**: Sistema de autenticação JWT para proteção de endpoints
- **Recomendações**: Funcionalidades para recomendação de livros baseadas em avaliações

### Arquitetura

A aplicação segue uma arquitetura em camadas (Layered Architecture):

```
┌─────────────────────────────────────────┐
│         API Layer (Routes)              │
│  FastAPI Endpoints + Middlewares       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      Service Layer (Business Logic)     │
│  Services: books, auth, stats, etc.    │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│    Repository Layer (Data Access)       │
│  Repositories: books, auth, etc.        │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│         Database Layer                  │
│  PostgreSQL + SQLAlchemy ORM           │
└─────────────────────────────────────────┘
```

#### Componentes Principais

- **FastAPI**: Framework web moderno e rápido para APIs
- **PostgreSQL**: Banco de dados relacional para persistência
- **SQLAlchemy**: ORM para interação com o banco de dados
- **JWT**: Autenticação baseada em tokens
- **BeautifulSoup4**: Web scraping de dados de livros
- **Prometheus**: Métricas de desempenho da API
- **Docker & Docker Compose**: Containerização e orquestração

#### Estrutura de Pastas

```
m1_ml_book_flow_api/
├── main.py                 # Ponto de entrada da aplicação
├── api/
│   ├── routes/            # Rotas da API (controllers)
│   ├── services/          # Lógica de negócio
│   ├── repositories/      # Acesso a dados
│   └── models/           # Modelos Pydantic (DTOs)
├── core/
│   ├── database.py       # Configuração do banco de dados
│   ├── models.py        # Modelos SQLAlchemy (ORM)
│   ├── security/        # Autenticação e autorização JWT
│   ├── middleware.py    # Middlewares HTTP
│   ├── handlers.py      # Handlers de exceção
│   └── logger.py        # Configuração de logging
└── data/                # Dados (raw, processed, samples)
```

---

## 📦 Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose instalados
- Git para clonar o repositório

### Instalação com Docker Compose (Recomendado)

1. **Clone o repositório:**
```bash
git clone <url-do-repositório>
cd m1-ml-book-flow-api
```

2. **Crie o arquivo `.env` na raiz do projeto:**
```bash
# Configurações do Servidor
PORT=8000
UVICORN_HOST=0.0.0.0
UVICORN_WORKERS=2

# Autenticação JWT
JWT_SECRET_KEY=sua_chave_secreta_aqui_altere_em_producao

# Configurações do Banco de Dados PostgreSQL
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres123
DB_NAME=books
```

**⚠️ IMPORTANTE:**
- `DB_HOST` deve ser `db` (nome do serviço no docker-compose, não `localhost`)
- `DB_NAME` deve estar definido (ex: `books`)
- `DB_USER` não deve conter espaços ou caracteres especiais
- Altere `JWT_SECRET_KEY` para um valor seguro em produção

3. **Construa e inicie os containers:**
```bash
docker compose up -d --build
```

A aplicação estará disponível em:
- **API**: `http://127.0.0.1:8000`
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **Métricas Prometheus**: `http://127.0.0.1:8000/metrics`

### Instalação Local (Desenvolvimento)

1. **Instale o Poetry** (gerenciador de dependências):
```bash
pip install poetry
```

2. **Instale as dependências:**
```bash
poetry install
```

3. **Ative o ambiente virtual:**
```bash
poetry shell
```

4. **Configure o arquivo `.env`** (mesmo formato do Docker)

5. **Execute a aplicação:**
```bash
uvicorn m1_ml_book_flow_api.main:app --reload --host 0.0.0.0 --port 8000
```

### Variáveis de Ambiente

| Variável | Descrição | Padrão | Obrigatório |
|----------|-----------|--------|-------------|
| `PORT` | Porta do servidor | `8000` | Sim |
| `UVICORN_HOST` | Host do servidor | `0.0.0.0` | Sim |
| `UVICORN_WORKERS` | Número de workers | `2` | Sim |
| `JWT_SECRET_KEY` | Chave secreta para tokens JWT | - | Sim |
| `DB_HOST` | Host do PostgreSQL | `db` | Sim |
| `DB_PORT` | Porta do PostgreSQL | `5432` | Sim |
| `DB_USER` | Usuário do PostgreSQL | - | Sim |
| `DB_PASSWORD` | Senha do PostgreSQL | - | Sim |
| `DB_NAME` | Nome do banco de dados | - | Sim |

---

## 🚀 Instruções para Execução

### Execução com Docker Compose

**Iniciar a aplicação:**
```bash
docker compose up -d
```

**Parar a aplicação:**
```bash
docker compose down
```

**Parar e remover volumes (⚠️ apaga dados do banco):**
```bash
docker compose down -v
```

**Ver logs:**
```bash
docker compose logs -f api
```

**Reconstruir após mudanças:**
```bash
docker compose up -d --build
```

### Acessar o Banco de Dados

#### Via psql (linha de comando):
```bash
psql -h localhost -p 5432 -U postgres -d books
```

#### Via ferramentas GUI (DBeaver, pgAdmin, etc):
```
Host: localhost
Port: 5432
Database: books
Username: postgres
Password: postgres123
```

#### URL de conexão:
```
postgresql://postgres:postgres123@localhost:5432/books
```

#### Via docker exec:
```bash
docker exec -it m1-ml-book-flow-db psql -U postgres -d books
```

### Troubleshooting

**Erro: "database does not exist" ou "password authentication failed"**
```bash
# Parar containers e remover volumes antigos
docker compose down -v

# Verificar arquivo .env
# Garantir que DB_USER, DB_PASSWORD, DB_NAME estão corretos

# Subir novamente
docker compose up -d --build
```

**Verificar credenciais atuais do container:**
```bash
docker exec m1-ml-book-flow-db printenv | grep POSTGRES
```

---

## 📚 Documentação das Rotas da API

### Base URL

Todas as rotas seguem o padrão: `http://127.0.0.1:8000/api/v1`

### Autenticação

A maioria dos endpoints requer autenticação via **Bearer Token JWT**. Para obter um token, utilize o endpoint `/api/v1/login`.

**Formato do Header:**
```
Authorization: Bearer <seu_token_jwt>
```

### Endpoints

#### 🔐 Autenticação

##### `POST /api/v1/login`
Realiza login e retorna tokens de acesso.

**Autenticação:** Não requerida

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

##### `POST /api/v1/refresh`
Renova o access token usando um refresh token válido.

**Autenticação:** Não requerida

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 📚 Livros

##### `GET /api/v1/books`
Lista todos os livros cadastrados.

**Autenticação:** Requerida

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Livro A",
    "author": "Autor A",
    "year": 2020,
    "category": "Ficção",
    "price": 29.9,
    "rating": 4.5,
    "available": true,
    "image": "url_a"
  }
]
```

##### `GET /api/v1/books/search`
Busca livros por título e/ou categoria.

**Autenticação:** Requerida

**Query Parameters:**
- `title` (opcional): Título ou parte do título
- `category` (opcional): Categoria ou parte da categoria

**Exemplo:**
```
GET /api/v1/books/search?title=Harry&category=Fiction
```

##### `GET /api/v1/books/price_range`
Busca livros por faixa de preço.

**Autenticação:** Requerida

**Query Parameters:**
- `min` (opcional): Preço mínimo
- `max` (opcional): Preço máximo

**Exemplo:**
```
GET /api/v1/books/price_range?min=10.0&max=50.0
```

##### `GET /api/v1/books/{book_id}`
Obtém detalhes completos de um livro.

**Autenticação:** Requerida

**Path Parameters:**
- `book_id` (int): ID do livro

**Response 200:**
```json
{
  "id": 1,
  "title": "Livro A",
  "author": "Autor A",
  "year": 2025,
  "score": 3.5,
  "price_without_tax": 37.90,
  "price_with_tax": 39.90,
  "tax": 2.00,
  "product_type": "Livro",
  "upc": "hgrf232",
  "available": true,
  "number_reviews": 67
}
```

##### `GET /api/v1/books/top-rated`
Lista os livros mais bem avaliados.

**Autenticação:** Requerida

**Query Parameters:**
- `number_items` (int, padrão: 10): Quantidade de livros a retornar

**Exemplo:**
```
GET /api/v1/books/top-rated?number_items=5
```

#### 📊 Estatísticas

##### `GET /api/v1/stats/overview`
Retorna estatísticas gerais dos livros.

**Autenticação:** Requerida

**Response 200:**
```json
{
  "total_books": 1000,
  "middle_price": 35.50,
  "distribution_ratings": {
    "4.0": 150,
    "4.5": 200,
    "5.0": 100
  }
}
```

##### `GET /api/v1/stats/categories`
Retorna estatísticas agrupadas por categoria.

**Autenticação:** Requerida

**Response 200:**
```json
[
  {
    "category_name": "Ficção",
    "quantity_books": 250,
    "category_price": 32.50
  },
  {
    "category_name": "Romance",
    "quantity_books": 180,
    "category_price": 28.75
  }
]
```

#### 📁 Categorias

##### `GET /api/v1/categories`
Lista todas as categorias disponíveis.

**Autenticação:** Requerida

**Response 200:**
```json
["Ficção", "Romance", "Suspense", "Terror"]
```

#### 🕷️ Web Scraping

##### `POST /api/v1/scraping/trigger`
Executa web scraping do site books.toscrape.com e armazena no banco.

**Autenticação:** Requerida

**Características:**
- Coleta: título, preço, rating, disponibilidade, categoria, imagem e autor
- Armazena automaticamente no PostgreSQL
- Atualiza livros existentes ou cria novos
- Processa página por página salvando incrementalmente

**Response 200:**
```json
{
  "message": "Scraping concluído com sucesso",
  "scraped_count": 1000,
  "saved_count": 1000,
  "pages_processed": 50
}
```

#### 💚 Health Check

##### `GET /api/v1/health`
Verifica o status de saúde da API.

**Autenticação:** Não requerida

**Response 200:**
```json
{
  "status": "ok",
  "total_books": 1000,
  "message": "API funcionando e dados acessíveis"
}
```

---

## 💡 Exemplos de Chamadas

### Exemplo 1: Login e Obter Token

```bash
# 1. Fazer login
curl -X POST "http://127.0.0.1:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }'

# Resposta:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer"
# }
```

### Exemplo 2: Listar Todos os Livros

```bash
# Substitua <TOKEN> pelo token obtido no login
curl -X GET "http://127.0.0.1:8000/api/v1/books" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 3: Buscar Livros por Título

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/search?title=Harry" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 4: Buscar Livros por Faixa de Preço

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/price_range?min=10.0&max=50.0" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 5: Obter Detalhes de um Livro

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/1" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 6: Obter Top 10 Livros Mais Avaliados

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/books/top-rated?number_items=10" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 7: Obter Estatísticas Gerais

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/stats/overview" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 8: Obter Estatísticas por Categoria

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/stats/categories" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 9: Listar Categorias

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/categories" \
  -H "Authorization: Bearer <TOKEN>"
```

### Exemplo 10: Executar Web Scraping

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/scraping/trigger" \
  -H "Authorization: Bearer <TOKEN>"

# Resposta:
# {
#   "message": "Scraping concluído com sucesso",
#   "scraped_count": 1000,
#   "saved_count": 1000,
#   "pages_processed": 50
# }
```

### Exemplo 11: Health Check

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/health"
```

### Exemplo 12: Renovar Token de Acesso

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<SEU_REFRESH_TOKEN>"
  }'
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação baseada em tokens
- **BeautifulSoup4** - Web scraping
- **Docker & Docker Compose** - Containerização
- **Prometheus** - Métricas e monitoramento
- **Poetry** - Gerenciamento de dependências

---

## 📝 Notas Importantes

- **Autenticação**: A maioria dos endpoints requer token JWT. Use o endpoint `/api/v1/login` para obter um token.
- **Tokens**: Access tokens expiram em 15 minutos. Use refresh tokens para renovar.
- **Web Scraping**: O processo de scraping salva dados incrementalmente (página por página) para evitar perda de dados.
- **Banco de Dados**: O PostgreSQL é inicializado automaticamente com Docker Compose. Dados são persistidos em volumes.
- **Logs**: Logs estruturados em JSON são gerados para todas as requisições e eventos.

---

## ✨ Boas Práticas Utilizadas

Este projeto implementa várias boas práticas de desenvolvimento de software para garantir qualidade, manutenibilidade, escalabilidade e segurança:

### 🏗️ Arquitetura e Design

1. **Arquitetura em Camadas (Layered Architecture)**
   - Separação clara entre Routes (Controllers), Services (Business Logic), Repositories (Data Access) e Database
   - Facilita manutenção, teste e evolução do código
   - Cada camada tem responsabilidades bem definidas

2. **Separação de Responsabilidades (SRP)**
   - Cada módulo tem uma responsabilidade única e bem definida
   - Services contêm lógica de negócio, Repositories gerenciam acesso a dados
   - Routes apenas orquestram requisições e respostas

3. **Dependency Injection**
   - Uso extensivo do sistema de Dependencies do FastAPI
   - Facilita testes unitários e isolamento de componentes
   - Exemplo: `get_db()`, `get_current_user()` como dependencies

### 📝 Código e Documentação

4. **Documentação Completa em Português**
   - Docstrings em todos os módulos, classes e funções
   - Documentação segue padrão Google Style
   - README completo com exemplos práticos

5. **Type Hints**
   - Uso de type hints em todas as funções
   - Melhora legibilidade e permite verificação estática
   - Facilita autocomplete em IDEs

6. **Modelos Pydantic para Validação**
   - Validação automática de dados de entrada/saída
   - Documentação automática via OpenAPI/Swagger
   - Type safety em tempo de execução

### 🔒 Segurança

7. **Autenticação JWT**
   - Tokens de acesso com expiração (15 minutos)
   - Refresh tokens com expiração maior (7 dias)
   - Separação entre access e refresh tokens

8. **Proteção de Endpoints**
   - Middleware para extração e validação de tokens
   - Dependency injection para verificação de autenticação
   - Tratamento seguro de erros sem expor informações sensíveis

9. **Variáveis de Ambiente**
   - Configurações sensíveis via variáveis de ambiente
   - Suporte a `.env` para desenvolvimento
   - Validação de variáveis obrigatórias no startup

### 📊 Logging e Monitoramento

10. **Logging Estruturado em JSON**
    - Logs em formato JSON para fácil parsing
    - Integração com ferramentas de análise (ELK, Splunk, etc.)
    - Campos padronizados: timestamp, level, service, version

11. **Request ID para Rastreamento**
    - Cada requisição recebe um UUID único
    - Header `X-Request-ID` na resposta
    - Facilita rastreamento de requisições em sistemas distribuídos

12. **Métricas com Prometheus**
    - Instrumentação automática de métricas HTTP
    - Endpoint `/metrics` para coleta
    - Header `X-Process-Time-ms` para tempo de processamento

### 🗄️ Banco de Dados

13. **ORM com SQLAlchemy**
    - Abstração de queries SQL
    - Migrações automáticas de schema
    - Pool de conexões otimizado (`pool_pre_ping=True`)

14. **Connection Pooling**
    - Reuso de conexões de banco de dados
    - Verificação automática de conexões expiradas
    - Timeout configurável para conexões

15. **Transações e Rollback**
    - Gerenciamento adequado de transações
    - Rollback automático em caso de erro
    - Sessões gerenciadas via Dependency Injection

16. **Salvamento Incremental**
    - No web scraping, dados são salvos página por página
    - Evita perda de dados em caso de erro
    - Reduz uso de memória em processos longos

### 🐳 Containerização e DevOps

17. **Docker Multi-Stage Build**
    - Imagens otimizadas e menores
    - Cache de dependências para builds rápidos
    - Separação entre dependências e código

18. **Docker Compose para Orquestração**
    - Serviços independentes e escaláveis
    - Health checks para dependências
    - Volumes nomeados para persistência

19. **Health Checks**
    - Health check do PostgreSQL no Docker Compose
    - Endpoint `/api/v1/health` para monitoramento
    - Aguarda dependências antes de iniciar

20. **Validação de Variáveis no Startup**
    - Dockerfile valida variáveis obrigatórias
    - Container falha rápido se variáveis ausentes
    - Erros claros sobre configuração faltante

### 🔧 Tratamento de Erros

21. **Handlers Centralizados de Exceção**
    - Tratamento unificado de erros HTTP
    - Respostas padronizadas em formato JSON
    - Logging detalhado de erros com stack trace

22. **Exceções Customizadas**
    - Exceções específicas para diferentes cenários
    - Mensagens de erro descritivas
    - Códigos de status HTTP apropriados

23. **Validação de Dados**
    - Validação automática via Pydantic
    - Mensagens de erro claras para validações
    - Handler específico para RequestValidationError

### ⚡ Performance e Escalabilidade

24. **Uvicorn com Workers**
    - Suporte a múltiplos workers para processamento paralelo
    - Configurável via variável de ambiente
    - Melhor uso de recursos em sistemas multi-core

25. **Middlewares Otimizados**
    - Middlewares leves e eficientes
    - Processamento mínimo de overhead
    - Headers customizados para métricas

26. **Lazy Loading de Dependências**
    - Imports apenas quando necessário
    - Redução de tempo de startup
    - Melhor organização de código

### 🧪 Testabilidade

27. **Separação de Camadas**
    - Cada camada pode ser testada independentemente
    - Services testáveis sem banco de dados
    - Repositories testáveis sem lógica de negócio

28. **Dependency Injection**
    - Fácil substituição de dependências em testes
    - Mocks e stubs podem ser injetados facilmente

### 📦 Gerenciamento de Dependências

29. **Poetry para Dependências**
    - Gerenciamento declarativo de dependências
    - Lock file para reproduzibilidade
    - Separação entre dependências de produção e desenvolvimento

30. **Versionamento Semântico**
    - Dependências com versões específicas
    - Evita breaking changes inesperados
    - Compatibilidade controlada

### 🚀 Observabilidade

31. **Logs Detalhados de Requisições**
    - Método HTTP, caminho, status code, duração
    - IP do cliente, user-agent, query params
    - Informações do usuário autenticado

32. **Logs de Eventos de Negócio**
    - Logs específicos para autenticação
    - Logs de eventos de scraping
    - Contexto rico para debugging

### 📚 Organização de Código

33. **Estrutura Modular**
    - Organização por funcionalidade
    - Módulos coesos e bem definidos
    - Fácil navegação e manutenção

34. **Nomenclatura Consistente**
    - Convenções de nomenclatura claras
    - Nomes descritivos e autoexplicativos
    - Padrão consistente em todo o projeto

### 🔄 Processamento Assíncrono

35. **Eventos de Startup/Shutdown**
    - Inicialização adequada do banco de dados
    - Cleanup de recursos no shutdown
    - Logging de eventos do ciclo de vida

### 🛡️ Resiliência

36. **Tratamento de Erros em Processos Longos**
    - Web scraping continua mesmo com erros em páginas individuais
    - Logs detalhados de progresso
    - Salvamento incremental previne perda total de dados

37. **Validação de Conexão de Banco**
    - Verificação antes de criar tabelas
    - Mensagens de erro claras sobre problemas de conexão
    - Graceful degradation quando apropriado

---

## 📄 Licença

MIT License

---

## 👥 Autores

- Marilise Morona <marymorona@gmail.com>
- Edi Vergis <evergis.ti@gmail.com>

---

## 🔗 Links Úteis

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **Métricas Prometheus**: `http://127.0.0.1:8000/metrics`