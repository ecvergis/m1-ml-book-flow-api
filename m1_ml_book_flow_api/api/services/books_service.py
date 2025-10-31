"""
Módulo de serviço para gerenciamento de livros.

Este módulo contém a lógica de negócio relacionada ao gerenciamento de livros,
incluindo listagem, busca, filtros e obtenção de detalhes. Funciona como
camada intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from m1_ml_book_flow_api.core.logger import get_logger, log_error
from ..models.Book import Book
from ..models.BookDetails import BookDetails
from ..repositories.books_repository import (
    list_books,
    search_books_by,
    get_book_by_id,
    search_books_by_range_price
)
from fastapi import HTTPException, status

books_logger = get_logger("books_service")

def list_all_books(db: Session) -> List[Book]:
    """
    Lista todos os livros cadastrados no sistema.

    Esta função busca todos os livros disponíveis no repositório e trata
    casos de erro, como quando não há livros cadastrados.

    Args:
        db (Session): Sessão do banco de dados

    Returns:
        List[Book]: Lista com todos os livros cadastrados no sistema.

    Raises:
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info("Fetching all books", extra={"event": "list_all_books_start"})
    
    try:
        books = list_books(db)
        if not books:
            books_logger.warning(
                "No books found",
                extra={
                    "event": "list_all_books_not_found",
                    "operation": "list_books"
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado")
        
        books_logger.info(
            "Books listed successfully",
            extra={
                "event": "list_all_books_success",
                "operation": "list_books",
                "books_count": len(books)
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(books_logger, e, "Error listing books", {"operation": "list_books"})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

def search_all_books(title: Optional[str] = None, category: Optional[str] = None, db: Session = None):
    """
    Busca livros por título e/ou categoria.

    Args:
        title (Optional[str]): Título do livro para busca (busca parcial)
        category (Optional[str]): Categoria do livro para busca (busca parcial)
        db (Session): Sessão do banco de dados

    Returns:
        List[Book]: Lista de livros que correspondem aos critérios de busca

    Raises:
        HTTPException 404: Se nenhum livro for encontrado
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info(
        "Searching books",
        extra={
            "event": "search_all_books_start",
            "title": title,
            "category": category
        }
    )
    
    try:
        books = search_books_by(title, category, db)
        if not books:
            books_logger.warning(
                "No books found for search criteria",
                extra={
                    "event": "search_all_books_not_found",
                    "title": title,
                    "category": category
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado")
        
        books_logger.info(
            "Books search completed successfully",
            extra={
                "event": "search_all_books_success",
                "title": title,
                "category": category,
                "books_count": len(books)
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(books_logger, e, "Error searching books", {"title": title, "category": category})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

def search_books_with_price(min: Optional[float] = None, max: Optional[float] = None, db: Session = None):
    """
    Busca livros por faixa de preço.

    Args:
        min (Optional[float]): Preço mínimo (inclusivo)
        max (Optional[float]): Preço máximo (inclusivo)
        db (Session): Sessão do banco de dados

    Returns:
        List[Book]: Lista de livros na faixa de preço especificada

    Raises:
        HTTPException 404: Se nenhum livro for encontrado na faixa de preço
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info(
        "Searching books by price range",
        extra={
            "event": "search_books_with_price_start",
            "min_price": min,
            "max_price": max
        }
    )
    
    try:
        books = search_books_by_range_price(min, max, db)
        if not books:
            books_logger.warning(
                "No books found for price range",
                extra={
                    "event": "search_books_with_price_not_found",
                    "min_price": min,
                    "max_price": max
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado na faixa de preço especificada")
        
        books_logger.info(
            "Books price search completed successfully",
            extra={
                "event": "search_books_with_price_success",
                "min_price": min,
                "max_price": max,
                "books_count": len(books)
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(books_logger, e, "Error searching books by price", {"min_price": min, "max_price": max})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")

def get_book_details(book_id: int, db: Session) -> BookDetails:
    """
    Obtém detalhes completos de um livro pelo ID.

    Args:
        book_id (int): ID único do livro
        db (Session): Sessão do banco de dados

    Returns:
        BookDetails: Detalhes completos do livro

    Raises:
        HTTPException 404: Se o livro não for encontrado
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info(
        "Fetching book details",
        extra={
            "event": "get_book_details_start",
            "book_id": book_id
        }
    )
    
    try:
        book = get_book_by_id(book_id, db)
        if not book:
            books_logger.warning(
                "Book not found",
                extra={
                    "event": "get_book_details_not_found",
                    "book_id": book_id
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
        
        books_logger.info(
            "Book details retrieved successfully",
            extra={
                "event": "get_book_details_success",
                "book_id": book_id
            }
        )
        return book
    except HTTPException:
        raise
    except Exception as e:
        log_error(books_logger, e, "Error getting book details", {"book_id": book_id})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")