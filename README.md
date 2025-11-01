# BookFlow API

API pública desenvolvida como projeto da Pós Tech em Machine Learning da FIAP. Fornece dados de livros processados para sistemas de recomendação e análise, integrando etapas de extração, transformação e disponibilização. Projetada com foco em escalabilidade, modularidade e reuso em modelos de aprendizado de máquina.

## 📋 Índice

- [Deploy e Demonstração](#-deploy-e-demonstração)
- [Descrição do Projeto e Arquitetura](#-descrição-do-projeto-e-arquitetura)
- [Pipeline de Dados e Machine Learning](#-pipeline-de-dados-e-machine-learning)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Instruções para Execução](#-instruções-para-execução)
- [Documentação das Rotas da API](#-documentação-das-rotas-da-api)
- [Exemplos de Chamadas](#-exemplos-de-chamadas)
- [Boas Práticas Utilizadas](#-boas-práticas-utilizadas)

---

## 🚀 Deploy e Demonstração

### 🌐 API em Produção

A API está disponível em produção no Heroku:

**🔗 [https://book-flow-api-e1ac898fc906.herokuapp.com/docs](https://book-flow-api-e1ac898fc906.herokuapp.com/docs)**

- **Documentação Interativa (Swagger)**: [/docs](https://book-flow-api-e1ac898fc906.herokuapp.com/docs)
- **Documentação Alternativa (ReDoc)**: [/redoc](https://book-flow-api-e1ac898fc906.herokuapp.com/redoc)
- **Health Check**: [/api/v1/health](https://book-flow-api-e1ac898fc906.herokuapp.com/api/v1/health)
- **Métricas**: [/metrics](https://book-flow-api-e1ac898fc906.herokuapp.com/metrics)

#### 🔐 Credenciais para Teste

Para testar a API em produção, use as seguintes credenciais no endpoint `/api/v1/login`:

```json
{
  "username": "admin",
  "password": "password123"
}
```

### 🎥 Vídeo de Apresentação

**🎬 [Link do Vídeo de Apresentação](_adicionar_link_do_video_aqui_)**

> 📝 _Vídeo demonstrando a arquitetura, funcionalidades e uso da API_

### 📊 Diagrama de Arquitetura

```mermaid
graph TB
    subgraph "Cliente"
        A[Browser/Postman/cURL]
    end
    
    subgraph "Heroku Cloud"
        subgraph "API Container Docker"
            B[FastAPI Application]
            C[Uvicorn Server]
            
            subgraph "Camada de Routes"
                D1[Auth Routes]
                D2[Books Routes]
                D3[Stats Routes]
                D4[Scraping Routes]
                D5[ML Routes]
            end
            
            subgraph "Camada de Services"
                E1[Auth Service]
                E2[Books Service]
                E3[Stats Service]
                E4[Scraping Service]
                E5[ML Service]
            end
            
            subgraph "Camada de Repositories"
                F1[Auth Repository]
                F2[Books Repository]
                F3[Stats Repository]
                F4[Scraping Repository]
            end
            
            subgraph "Core Components"
                G1[JWT Security]
                G2[Middleware]
                G3[Logger]
                G4[Exception Handlers]
            end
        end
        
        H[PostgreSQL Database]
        I[Prometheus Metrics]
    end
    
    subgraph "External Services"
        J[books.toscrape.com]
    end
    
    A -->|HTTPS Request| B
    B --> C
    C --> D1 & D2 & D3 & D4 & D5
    
    D1 --> E1
    D2 --> E2
    D3 --> E3
    D4 --> E4
    D5 --> E5
    
    E1 --> F1
    E2 --> F2
    E3 --> F3
    E4 --> F4
    
    E1 & E2 & E3 & E4 & E5 --> G1
    B --> G2 & G3 & G4
    
    F1 & F2 & F3 & F4 -->|SQLAlchemy ORM| H
    E4 -->|Web Scraping| J
    
    B -->|Expose Metrics| I
    
    style A fill:#e1f5ff
    style B fill:#ffe1e1
    style H fill:#e1ffe1
    style J fill:#fff5e1
    style I fill:#f0e1ff
```

#### Fluxo de uma Requisição

1. **Cliente** → Envia requisição HTTPS para a API
2. **Middleware** → Processa logging, autenticação e métricas
3. **Routes** → Recebe a requisição e valida dados (Pydantic)
4. **Services** → Executa lógica de negócio
5. **Repositories** → Acessa dados no PostgreSQL via SQLAlchemy
6. **Response** → Retorna dados formatados em JSON

#### Componentes Principais

| Componente | Tecnologia | Função |
|------------|-----------|---------|
| **API Framework** | FastAPI | Framework web moderno e rápido |
| **Web Server** | Uvicorn | Servidor ASGI de alta performance |
| **Database** | PostgreSQL | Banco de dados relacional |
| **ORM** | SQLAlchemy | Mapeamento objeto-relacional |
| **Authentication** | JWT | Tokens de autenticação seguros |
| **Containerization** | Docker | Isolamento e portabilidade |
| **Cloud Platform** | Heroku | Hospedagem e deploy automático |
| **Monitoring** | Prometheus | Métricas e observabilidade |
| **Web Scraping** | BeautifulSoup4 | Extração de dados web |

---

## 🏗️ Descrição do Projeto e Arquitetura

### Descrição

O BookFlow API é uma API REST desenvolvida em Python com FastAPI que fornece:

- **Gerenciamento de Livros**: CRUD completo para livros com busca avançada
- **Estatísticas**: Análises e métricas sobre os livros cadastrados
- **Web Scraping**: Coleta automática de dados de livros de sites externos
- **Autenticação**: Sistema de autenticação JWT para proteção de endpoints
- **Machine Learning**: Endpoints especializados para consumo por modelos de ML
- **Features Engineering**: Dados processados e transformados para ML
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
├── ml/                  # Módulo de Machine Learning
└── data/                # Dados (raw, processed, samples)
```

---

## 🤖 Pipeline de Dados e Machine Learning

### 📊 Pipeline Completo: Da Ingestão ao Consumo

A BookFlow API implementa um pipeline completo de dados pensado para Machine Learning:

```mermaid
graph LR
    subgraph "1. INGESTÃO"
        A[Web Scraping] -->|books.toscrape.com| B[Raw Data]
        A1[Upload Manual] --> B
        A2[APIs Externas] --> B
    end
    
    subgraph "2. PROCESSAMENTO"
        B --> C[Validação]
        C --> D[Limpeza]
        D --> E[Transformação]
        E --> F[Feature Engineering]
    end
    
    subgraph "3. ARMAZENAMENTO"
        F --> G[PostgreSQL]
        G --> H[Dados Estruturados]
    end
    
    subgraph "4. API REST"
        H --> I[Endpoints CRUD]
        H --> J[Endpoints ML]
        H --> K[Endpoints Stats]
    end
    
    subgraph "5. CONSUMO"
        I --> L[Aplicações Web]
        I --> M[Mobile Apps]
        J --> N[Modelos de ML]
        J --> O[Notebooks Jupyter]
        J --> P[Pipelines MLOps]
        K --> Q[Dashboards BI]
    end
    
    style A fill:#ff9999
    style F fill:#99ff99
    style G fill:#9999ff
    style J fill:#ffcc99
    style N fill:#ff99ff
```

### 🎯 Cenário de Uso para Cientistas de Dados

A API foi projetada especificamente para facilitar o trabalho de cientistas de dados e engenheiros de ML:

#### 1. **Coleta Rápida de Dados**
```python
import requests

# Obter dados de treinamento já processados
response = requests.get(
    "https://book-flow-api.herokuapp.com/api/v1/ml/training-data",
    headers={"Authorization": f"Bearer {token}"}
)
dataset = response.json()
```

#### 2. **Features Prontas para Uso**
```python
# Obter features engineering já aplicadas
response = requests.get(
    "https://book-flow-api.herokuapp.com/api/v1/ml/features",
    headers={"Authorization": f"Bearer {token}"}
)
features = response.json()

# Features incluem:
# - title_length (comprimento do título)
# - author_encoded (autor codificado)
# - year_normalized (ano normalizado)
# - category_encoded (categoria one-hot)
# - price_normalized (preço normalizado [0-1])
# - rating_normalized (rating normalizado [0-1])
# - availability_flag (disponível: 1/0)
# - popularity_score (score de popularidade)
```

#### 3. **Experimentação Rápida**
```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Carregar dados
response = requests.get(url, headers=headers)
data = response.json()

# Preparar dados
df = pd.DataFrame(data['records'])
X = df[data['feature_names']]
y = df['rating']

# Treinar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Avaliar
score = model.score(X_test, y_test)
print(f"R² Score: {score}")
```

#### 4. **Deploy de Modelos**
```python
# Enviar predições de volta para a API
predictions_request = {
    "model_type": "rating",
    "input_features": {
        "title_length": 45,
        "author_encoded": 123,
        "year_normalized": 0.85,
        "price_normalized": 0.32
    }
}

response = requests.post(
    "https://book-flow-api.herokuapp.com/api/v1/ml/predictions",
    json=predictions_request,
    headers={"Authorization": f"Bearer {token}"}
)
```

### 🔌 Endpoints de Machine Learning

A API fornece endpoints especializados para ML:

| Endpoint | Método | Descrição | Uso |
|----------|--------|-----------|-----|
| `/api/v1/ml/features` | GET | Features processadas | Obter dados transformados para ML |
| `/api/v1/ml/training-data` | GET | Dataset de treinamento | Dataset completo com train/test/val split |
| `/api/v1/ml/predictions` | POST | Realizar predições | Inferência usando modelos treinados |

#### Exemplo: Obter Features

**Request:**
```bash
curl -X GET "https://book-flow-api.herokuapp.com/api/v1/ml/features" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**
```json
{
  "total_records": 1000,
  "feature_names": [
    "title_length",
    "author_encoded",
    "year_normalized",
    "category_encoded",
    "price_normalized",
    "rating_normalized",
    "availability_flag",
    "popularity_score"
  ],
  "records": [
    {
      "book_id": 1,
      "title_length": 45,
      "author_encoded": 123,
      "year_normalized": 0.85,
      "category_encoded": 2,
      "price_normalized": 0.32,
      "rating_normalized": 0.9,
      "availability_flag": 1,
      "popularity_score": 0.78
    }
  ],
  "metadata": {
    "encoding_mappings": {...},
    "normalization_params": {...}
  }
}
```

#### Exemplo: Obter Dados de Treinamento

**Response inclui:**
- Dataset completo com features e targets
- Sugestões de split (train/test/validation)
- Estatísticas do dataset
- Mapeamentos e normalizações aplicadas
- Informações sobre desbalanceamento de classes

#### Exemplo: Fazer Predições

**Request:**
```json
{
  "model_type": "rating",
  "input_features": {
    "title_length": 45,
    "author_encoded": 123,
    "year_normalized": 0.85,
    "category_encoded": 2,
    "price_normalized": 0.32,
    "availability_flag": 1,
    "popularity_score": 0.78
  }
}
```

**Modelos Suportados:**
- `rating`: Predição de avaliação de livros
- `price`: Predição de preço de livros
- `category`: Classificação de categoria
- `recommendation`: Sistema de recomendação

### 🚀 Plano de Integração com Modelos de ML

#### Fase 1: Consumo Atual (✅ Implementado)
- ✅ Endpoints para obter dados processados
- ✅ Features engineering automatizado
- ✅ Formato JSON padronizado
- ✅ Autenticação JWT para segurança

#### Fase 2: Integração com MLOps (🚧 Planejado)
```python
# Exemplo de integração futura com MLflow
import mlflow
import requests

# Treinar modelo
with mlflow.start_run():
    # Obter dados da API
    data = requests.get(api_url, headers=headers).json()
    
    # Treinar modelo
    model = train_model(data)
    
    # Registrar no MLflow
    mlflow.sklearn.log_model(model, "book_rating_model")
    
    # Deploy automático
    mlflow.deployments.create(
        name="book-rating",
        model_uri=f"models:/book_rating_model/production"
    )
```

#### Fase 3: Integração com Cloud ML (🔮 Futuro)
- AWS SageMaker
- Google Cloud AI Platform
- Azure Machine Learning
- Vertex AI

#### Fase 4: Real-time Inference (🔮 Futuro)
- Endpoint de inferência em tempo real
- Cache de predições frequentes
- Batch predictions
- A/B testing de modelos

### 📈 Arquitetura para Escalabilidade Futura

A aplicação foi projetada pensando em escalabilidade:

#### Escalabilidade Horizontal

```
                                ┌─────────────┐
                                │   Load      │
                                │  Balancer   │
                                └──────┬──────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
               ┌────▼────┐        ┌────▼────┐       ┌────▼────┐
               │  API    │        │  API    │       │  API    │
               │Instance │        │Instance │       │Instance │
               │   #1    │        │   #2    │       │   #N    │
               └────┬────┘        └────┬────┘       └────┬────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                              ┌────────▼─────────┐
                              │   PostgreSQL     │
                              │   (Read Replicas)│
                              └──────────────────┘
```

#### Componentes Preparados para Escala

1. **Stateless API**
   - Nenhum estado armazenado na aplicação
   - Fácil replicação horizontal
   - Session management via JWT

2. **Connection Pooling**
   - Pool de conexões otimizado
   - Reuso eficiente de conexões
   - Timeout configurável

3. **Containerização**
   - Docker para portabilidade
   - Kubernetes-ready (futuramente)
   - Auto-scaling configurável

4. **Cache Layer (Planejado)**
   ```
   Cliente → API → Redis Cache → PostgreSQL
   ```
   - Redis para cache de queries frequentes
   - TTL configurável
   - Invalidação inteligente

5. **Assíncrono (Planejado)**
   - Celery para tarefas assíncronas
   - RabbitMQ/Redis como message broker
   - Background jobs para scraping e ML

#### Métricas e Monitoramento

- ✅ **Prometheus**: Métricas de performance
- ✅ **Logging estruturado**: Logs em JSON
- ✅ **Request ID**: Rastreamento de requisições
- 🚧 **Grafana**: Dashboards visuais (planejado)
- 🚧 **Alerting**: Alertas automáticos (planejado)

#### Plano de Escalabilidade

| Uso Atual | 0-1K req/min | Heroku Single Dyno |
| Fase 1 | 1K-10K req/min | Multiple Dynos + Postgres Scaling |
| Fase 2 | 10K-100K req/min | Kubernetes + Redis + Read Replicas |
| Fase 3 | 100K+ req/min | Multi-region + CDN + Sharding |

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