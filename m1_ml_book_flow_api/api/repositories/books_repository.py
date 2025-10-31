"""
Módulo de repositório para gerenciamento de livros.

Este módulo contém funções para buscar, listar e filtrar livros a partir do
banco de dados PostgreSQL. Serve como camada de acesso aos dados de livros.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from m1_ml_book_flow_api.api.models.Book import Book
from m1_ml_book_flow_api.core.models import BookDB
from m1_ml_book_flow_api.core.database import get_db

def _convert_book_db_to_book(book_db: BookDB) -> Book:
    """
    Converte um modelo BookDB (SQLAlchemy) para um modelo Book (Pydantic).
    
    Args:
        book_db (BookDB): Instância do modelo de banco de dados
        
    Returns:
        Book: Instância do modelo Pydantic
    """
    return Book(
        id=book_db.id,
        title=book_db.title,
        author=book_db.author or "",
        year=book_db.year or 0,
        category=book_db.category or "",
        price=book_db.price,
        rating=book_db.rating or 0.0,
        available=book_db.available,
        image=book_db.image or ""
    )

def list_books(db: Session = None) -> List[Book]:
    """
    Lista todos os livros disponíveis no banco de dados.

    Args:
        db (Session, optional): Sessão do banco de dados. Se não fornecida, cria uma nova.

    Returns:
        List[Book]: Lista com todos os livros cadastrados no sistema.
    """
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        try:
            books_db = db.query(BookDB).all()
            return [_convert_book_db_to_book(book) for book in books_db]
        finally:
            db.close()
    else:
        books_db = db.query(BookDB).all()
        return [_convert_book_db_to_book(book) for book in books_db]

def search_books_by(title: Optional[str] = None, category: Optional[str] = None, db: Session = None) -> List[Book]:
    """
    Busca livros por título e/ou categoria no banco de dados.

    A busca por título é feita de forma parcial (case-insensitive), ou seja,
    se o título fornecido estiver contido no título do livro, ele será retornado.
    O mesmo vale para a categoria.

    Args:
        title (Optional[str]): Título ou parte do título para filtrar. Se None, não filtra por título.
        category (Optional[str]): Categoria ou parte da categoria para filtrar. Se None, não filtra por categoria.
        db (Session, optional): Sessão do banco de dados. Se não fornecida, cria uma nova.

    Returns:
        List[Book]: Lista de livros que correspondem aos critérios de busca.
                   Se ambos os parâmetros forem None, retorna todos os livros.
    """
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        try:
            query = db.query(BookDB)
            
            filters = []
            if title:
                filters.append(BookDB.title.ilike(f"%{title}%"))
            if category:
                filters.append(BookDB.category.ilike(f"%{category}%"))
            
            if filters:
                query = query.filter(and_(*filters))
            
            books_db = query.all()
            return [_convert_book_db_to_book(book) for book in books_db]
        finally:
            db.close()
    else:
        query = db.query(BookDB)
        
        filters = []
        if title:
            filters.append(BookDB.title.ilike(f"%{title}%"))
        if category:
            filters.append(BookDB.category.ilike(f"%{category}%"))
        
        if filters:
            query = query.filter(and_(*filters))
        
        books_db = query.all()
        return [_convert_book_db_to_book(book) for book in books_db]

def search_books_by_range_price(min_price: float = 0.0, max_price: Optional[float] = None, db: Session = None) -> List[Book]:
    """
    Busca livros por faixa de preço no banco de dados.

    Retorna todos os livros cujo preço está entre min_price (inclusivo) e max_price (inclusivo).
    Se max_price for None, retorna todos os livros com preço maior ou igual a min_price.

    Args:
        min_price (float): Preço mínimo (inclusivo). Padrão: 0.0
        max_price (Optional[float]): Preço máximo (inclusivo). Se None, não há limite superior.
        db (Session, optional): Sessão do banco de dados. Se não fornecida, cria uma nova.

    Returns:
        List[Book]: Lista de livros que estão na faixa de preço especificada.
    """
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        try:
            query = db.query(BookDB).filter(BookDB.price >= min_price)
            
            if max_price is not None:
                query = query.filter(BookDB.price <= max_price)
            
            books_db = query.all()
            return [_convert_book_db_to_book(book) for book in books_db]
        finally:
            db.close()
    else:
        query = db.query(BookDB).filter(BookDB.price >= min_price)
        
        if max_price is not None:
            query = query.filter(BookDB.price <= max_price)
        
        books_db = query.all()
        return [_convert_book_db_to_book(book) for book in books_db]

def get_book_by_id(book_id: int, db: Session = None):
    """
    Obtém detalhes completos de um livro pelo ID do banco de dados.

    Args:
        book_id (int): ID único do livro a ser buscado.
        db (Session, optional): Sessão do banco de dados. Se não fornecida, cria uma nova.

    Returns:
        dict: Dicionário com detalhes completos do livro se encontrado, None caso contrário.
              Contém campos: id, title, author, year, score, price_without_tax,
              price_with_tax, tax, product_type, upc, available, number_reviews.
    """
    if db is None:
        db_gen = get_db()
        db = next(db_gen)
        try:
            book_db = db.query(BookDB).filter(BookDB.id == book_id).first()
            if book_db:
                # Simulando campos adicionais que não existem no modelo atual
                # mas são esperados pela API (para compatibilidade)
                return {
                    "id": book_db.id,
                    "title": book_db.title,
                    "author": book_db.author or "",
                    "year": book_db.year or 0,
                    "score": book_db.rating or 0.0,
                    "price_without_tax": round(book_db.price * 0.9, 2),  # Simulando preço sem imposto
                    "price_with_tax": book_db.price,
                    "tax": round(book_db.price * 0.1, 2),  # Simulando 10% de imposto
                    "product_type": "Livro",
                    "upc": f"UPC{book_db.id:06d}",  # Gerando UPC baseado no ID
                    "available": book_db.available,
                    "number_reviews": int(book_db.rating * 20) if book_db.rating else 0  # Simulando número de reviews
                }
            return None
        finally:
            db.close()
    else:
        book_db = db.query(BookDB).filter(BookDB.id == book_id).first()
        if book_db:
            return {
                "id": book_db.id,
                "title": book_db.title,
                "author": book_db.author or "",
                "year": book_db.year or 0,
                "score": book_db.rating or 0.0,
                "price_without_tax": round(book_db.price * 0.9, 2),
                "price_with_tax": book_db.price,
                "tax": round(book_db.price * 0.1, 2),
                "product_type": "Livro",
                "upc": f"UPC{book_db.id:06d}",
                "available": book_db.available,
                "number_reviews": int(book_db.rating * 20) if book_db.rating else 0
            }
        return None