"""
Módulo de modelos de dados do banco de dados.

Este módulo define os modelos SQLAlchemy que representam as tabelas do banco de dados.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from m1_ml_book_flow_api.core.database import Base

class BookDB(Base):
    """
    Modelo que representa a tabela de livros no banco de dados.
    
    Esta classe mapeia a tabela 'books' no PostgreSQL e contém todos os
    campos de informações sobre os livros coletados via scraping.
    
    Attributes:
        id (int): ID único do livro (chave primária)
        title (str): Título do livro (obrigatório, indexado)
        author (str, optional): Nome do autor
        year (int, optional): Ano de publicação
        category (str, optional): Categoria do livro (indexado)
        price (float): Preço do livro (obrigatório)
        rating (float, optional): Avaliação em estrelas (1.0 a 5.0)
        available (bool): Se o livro está disponível (default: True)
        image (str, optional): URL da imagem da capa do livro
        created_at (datetime): Data e hora de criação do registro (automático)
        updated_at (datetime, optional): Data e hora da última atualização (automático)
    """
    __tablename__ = "books"

    # Chave primária
    id = Column(Integer, primary_key=True, index=True)
    
    # Informações básicas do livro
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    category = Column(String, nullable=True, index=True)
    
    # Informações comerciais
    price = Column(Float, nullable=False)
    rating = Column(Float, nullable=True)
    available = Column(Boolean, default=True)
    image = Column(String, nullable=True)
    
    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

