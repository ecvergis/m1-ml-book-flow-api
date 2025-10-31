"""
Módulo principal da aplicação BookFlow API.

Este módulo é o ponto de entrada principal da aplicação FastAPI. Configura e inicializa
todos os componentes necessários para a execução da API, incluindo:

- Carregamento de variáveis de ambiente
- Configuração da aplicação FastAPI
- Registro de middlewares (logging, contexto, métricas)
- Registro de rotas da API
- Configuração de handlers de exceção
- Instrumentação Prometheus para métricas
- Inicialização do banco de dados
- Eventos de startup e shutdown

A aplicação fornece uma API REST para gerenciamento de livros, incluindo funcionalidades
de autenticação, estatísticas, categorias, web scraping e recomendações.
"""
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from .api.routes import books, auth, health, stats_overview, categories, stats_categories, top_rating, scraping
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from m1_ml_book_flow_api.core.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from fastapi.security import HTTPBearer
from .core.middleware import LoggingMiddleware, RequestContextMiddleware, MetricsMiddleware
from .core.logger import Logger
from .core.database import init_db

# Instância HTTPBearer para validação de tokens JWT (não utilizada diretamente aqui,
# mas disponível para uso em outras partes da aplicação)
security = HTTPBearer()

# Configuração da aplicação FastAPI
app = FastAPI(
    title="BookFlow API",
    description="""
API pública desenvolvida como projeto da Pós Tech em Machine Learning da FIAP. Fornece dados de livros processados para sistemas de recomendação e análise, integrando etapas de extração, transformação e disponibilização. Projetada com foco em escalabilidade, modularidade e reuso em modelos de aprendizado de máquina.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Registro de middlewares (ordem importa - são executados na ordem inversa de registro)
# LoggingMiddleware: Registra todas as requisições HTTP com detalhes completos
app.add_middleware(LoggingMiddleware)
# RequestContextMiddleware: Extrai informações de autenticação do token JWT
app.add_middleware(RequestContextMiddleware)
# MetricsMiddleware: Adiciona métricas de desempenho às respostas
app.add_middleware(MetricsMiddleware)

# Prefixo base para todas as rotas da API
prefix_api = "/api/v1"

# Registro de todas as rotas da API com prefixo e tags para organização
app.include_router(top_rating.router, prefix=prefix_api, tags=["top_rated"])
app.include_router(books.router, prefix=prefix_api, tags=["books"])
app.include_router(categories.router, prefix=prefix_api, tags=["categories"])
app.include_router(auth.router, prefix=prefix_api, tags=["auth"])
app.include_router(health.router, prefix=prefix_api, tags=["health"])
app.include_router(stats_overview.router, prefix=prefix_api, tags=["stats_overview"])
app.include_router(stats_categories.router, prefix=prefix_api, tags=["stats_categories"])
app.include_router(scraping.router, prefix=prefix_api, tags=["scraping"])

# Registro de handlers de exceção para tratamento centralizado de erros
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Instrumentação Prometheus para coleta de métricas da API
# Expõe endpoint /metrics para scraping pelo Prometheus
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.on_event("startup")
async def startup_event():
    """
    Evento executado durante a inicialização da aplicação.

    Este evento é executado uma vez quando a aplicação FastAPI inicia, antes de
    aceitar requisições. Realiza as seguintes operações:

    1. Registra log de inicialização
    2. Importa modelos do banco de dados para garantir que sejam registrados
    3. Inicializa o banco de dados criando todas as tabelas necessárias
    4. Registra log de sucesso ou erro da inicialização do banco

    Se a inicialização do banco de dados falhar, o erro é registrado mas a
    aplicação continua iniciando. Isso permite que problemas de conexão sejam
    tratados em tempo de execução.
    """
    Logger.info("Starting BookFlow API", extra={"event": "startup", "version": "1.0.0", "service": "book-flow-api"})
    
    # Inicializa tabelas do banco de dados
    try:
        # Importa modelos antes de inicializar o banco para garantir que sejam registrados
        from m1_ml_book_flow_api.core.models import BookDB  # noqa: F401
        init_db()
        Logger.info("Database initialized", extra={"event": "database_init", "service": "book-flow-api"})
    except Exception as e:
        Logger.exception(f"Error initializing database: {e}", extra={"event": "database_init_error", "service": "book-flow-api"})

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado durante o encerramento da aplicação.

    Este evento é executado quando a aplicação FastAPI está sendo encerrada,
    permitindo realizar operações de limpeza e finalização.

    Atualmente registra um log informando o encerramento da aplicação.
    Operações adicionais como fechamento de conexões ou salvamento de estado
    podem ser adicionadas aqui conforme necessário.
    """
    Logger.info("Shutting down BookFlow API", extra={"event": "shutdown", "service": "book-flow-api", "version": "1.0.0"})
