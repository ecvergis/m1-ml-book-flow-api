"""
Módulo de configuração e gerenciamento do banco de dados.

Este módulo configura a conexão com PostgreSQL usando SQLAlchemy e fornece
funções para gerenciar sessões e inicializar o banco de dados.
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Configurações de conexão com o banco de dados
# O Heroku fornece DATABASE_URL, então priorizamos isso
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Heroku fornece postgres:// mas SQLAlchemy 2.0+ requer postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Configuração local via variáveis individuais
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
    DB_NAME = os.getenv("DB_NAME", "books")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Engine SQLAlchemy com configurações otimizadas
# pool_pre_ping: verifica conexões antes de usar para evitar erros de conexão expirada
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 10})

# Factory de sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos SQLAlchemy (ORM)
Base = declarative_base()

def get_db():
    """
    Dependency para obter sessão do banco de dados.
    
    Esta função é usada como dependency do FastAPI para injetar sessões
    do banco de dados nas rotas. A sessão é fechada automaticamente após
    o uso (usando yield).
    
    Yields:
        Session: Sessão do banco de dados SQLAlchemy
        
    Example:
        @router.get("/endpoint")
        def minha_rota(db: Session = Depends(get_db)):
            # usar db aqui
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database_exists() -> bool:
    """
    Verifica se o banco de dados existe e está acessível.
    
    Tenta executar uma query simples para validar a conexão.
    
    Returns:
        bool: True se o banco está acessível, False caso contrário
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return True
    except OperationalError as e:
        print(f"Erro de conexão com o banco de dados: {e}")
        return False

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    
    Esta função cria automaticamente todas as tabelas definidas nos modelos
    SQLAlchemy (que herdam de Base). Deve ser chamada no startup da aplicação.
    
    Raises:
        Exception: Se o banco de dados não estiver acessível ou houver erro na criação
    """
    # Importa modelos para garantir que sejam registrados com Base
    from m1_ml_book_flow_api.core.models import BookDB  # noqa: F401
    
    # Verifica conexão antes de criar tabelas
    if not check_database_exists():
        raise Exception(f"Banco de dados {DB_NAME} não está acessível. Verifique se o PostgreSQL está rodando e o banco existe.")
    
    # Cria todas as tabelas definidas nos modelos
    Base.metadata.create_all(bind=engine)
