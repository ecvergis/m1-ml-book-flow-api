import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "pass")
DB_NAME = os.getenv("DB_NAME", "books")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 10})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database_exists():
    """Check if database exists and is accessible"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return True
    except OperationalError as e:
        print(f"Database connection error: {e}")
        return False

def init_db():
    """Create all tables"""
    # Import models to ensure they're registered with Base
    from m1_ml_book_flow_api.core.models import BookDB  # noqa: F401
    
    # Check database connection first
    if not check_database_exists():
        raise Exception(f"Database {DB_NAME} is not accessible. Please ensure PostgreSQL is running and the database exists.")
    
    Base.metadata.create_all(bind=engine)
