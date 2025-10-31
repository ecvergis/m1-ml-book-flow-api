"""
Módulo de serviço para gerenciamento de livros.

Este módulo contém a lógica de negócio relacionada ao gerenciamento de livros,
incluindo listagem, busca, filtros e obtenção de detalhes. Funciona como
camada intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from typing import List, Optional
from m1_ml_book_flow_api.core.logger import get_logger, log_error
from ..models.Book import Book
from ..repositories.books_repository import (
    list_books,
    search_books_by,
    get_book_by_id,
    search_books_by_range_price
)
from fastapi import HTTPException, status

books_logger = get_logger("books_service")

def list_all_books() -> List[Book]:
    """
    Lista todos os livros cadastrados no sistema.

    Esta função busca todos os livros disponíveis no repositório e trata
    casos de erro, como quando não há livros cadastrados.

    Returns:
        List[Book]: Lista com todos os livros cadastrados no sistema.

    Raises:
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info("Fetching all books", extra={"event": "list_all_books_start"})
    
    try:
        books = list_books()
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
                "books_count": len(books),
                "operation": "list_books"
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="list_all_books",
            event="list_all_books_error"
        )
        raise

def search_all_books(title: Optional[str] = None, category: Optional[str] = None):
    """
    Busca livros por título e/ou categoria.

    Permite filtrar livros usando critérios de busca parcial (case-insensitive).
    Pode buscar apenas por título, apenas por categoria, ou por ambos simultaneamente.

    Args:
        title (Optional[str]): Título ou parte do título para filtrar. Se None, não filtra por título.
        category (Optional[str]): Categoria ou parte da categoria para filtrar. Se None, não filtra por categoria.

    Returns:
        List[Book]: Lista de livros que correspondem aos critérios de busca.
                   Se ambos os parâmetros forem None, retorna todos os livros.

    Raises:
        HTTPException 404: Se nenhum livro corresponder aos critérios de busca
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    books_logger.info(
        "Searching books by criteria",
        extra={
            "event": "search_all_books_start",
            "title": title,
            "category": category
        }
    )
    
    try:
        books = search_books_by(title=title, category=category)
        if not books:
            books_logger.warning(
                "No books found with given criteria",
                extra={
                    "event": "search_all_books_not_found",
                    "title": title,
                    "category": category,
                    "operation": "search_books_by"
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado")
        
        books_logger.info(
            "Books found successfully",
            extra={
                "event": "search_all_books_success",
                "books_count": len(books),
                "title": title,
                "category": category,
                "operation": "search_books_by"
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="search_all_books",
            title=title,
            category=category,
            event="search_all_books_error"
        )
        raise

def search_books_with_price(min: Optional[float] = None, max: Optional[float] = None):
    """
    Busca livros por faixa de preço.

    Retorna todos os livros cujo preço está entre min (inclusivo) e max (inclusivo).
    Se max for None, retorna todos os livros com preço maior ou igual a min.
    Se min for None, retorna todos os livros com preço menor ou igual a max.

    Args:
        min (Optional[float]): Preço mínimo (inclusivo). Se None, usa 0.0 como padrão.
        max (Optional[float]): Preço máximo (inclusivo). Se None, não há limite superior.

    Returns:
        List[Book]: Lista de livros que estão na faixa de preço especificada.
                   Se ambos os parâmetros forem None, retorna todos os livros com preço >= 0.0.

    Raises:
        HTTPException 404: Se nenhum livro corresponder à faixa de preço especificada
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    min_price = 0.0 if min is None else min
    max_price = max  # pode continuar None
    
    books_logger.info(
        "Searching books by price range",
        extra={
            "event": "search_books_with_price_start",
            "min_price": min_price,
            "max_price": max_price
        }
    )
    
    try:
        books = search_books_by_range_price(min_price=min_price, max_price=max_price)
        
        if not books:
            books_logger.warning(
                "No books found in price range",
                extra={
                    "event": "search_books_with_price_not_found",
                    "min_price": min_price,
                    "max_price": max_price,
                    "operation": "search_books_by_range_price"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro encontrado"
            )
        
        books_logger.info(
            "Books found in price range",
            extra={
                "event": "search_books_with_price_success",
                "books_count": len(books),
                "min_price": min_price,
                "max_price": max_price,
                "operation": "search_books_by_range_price"
            }
        )
        return books
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="search_books_with_price",
            min_price=min_price,
            max_price=max_price,
            event="search_books_with_price_error"
        )
        raise

def get_book_details(book_id: int) -> Book:
    """
    Obtém detalhes completos de um livro pelo ID.

    Busca um livro específico no repositório usando seu ID e retorna
    informações detalhadas do mesmo.

    Args:
        book_id (int): ID único do livro a ser buscado.

    Returns:
        Book: Objeto com detalhes completos do livro.

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
        book = get_book_by_id(book_id)
        if not book:
            books_logger.warning(
                "Book not found",
                extra={
                    "event": "get_book_details_not_found",
                    "book_id": book_id,
                    "operation": "get_book_by_id"
                }
            )
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
        
        books_logger.info(
            "Book details fetched successfully",
            extra={
                "event": "get_book_details_success",
                "book_id": book_id,
                "operation": "get_book_by_id"
            }
        )
        return book
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="get_book_details",
            book_id=book_id,
            event="get_book_details_error"
        )
        raise