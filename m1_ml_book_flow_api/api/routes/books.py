"""
Módulo de rotas para endpoints de livros.

Este módulo define as rotas da API relacionadas ao gerenciamento de livros,
incluindo listagem, busca, filtros por preço e obtenção de detalhes.
"""
# api/routes/books.py
from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from ..services.books_service import (
    list_all_books,
    search_all_books,
    get_book_details,
    search_books_with_price
)
from m1_ml_book_flow_api.api.models.Book import Book
from m1_ml_book_flow_api.api.models.BookDetails import BookDetails
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.database import get_db
from m1_ml_book_flow_api.core.errors import ErrorResponse

# Router com dependência de autenticação em todas as rotas
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

# GET /api/v1/books
@router.get(
    "/books",
    response_model=List[Book],
    responses={
        404: {"description": "Nenhum livro encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Listar todos os livros",
    description="Retorna uma lista de livros cadastrados."
)
def list_books(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Lista todos os livros cadastrados no sistema.

    Este endpoint retorna uma lista completa de todos os livros disponíveis,
    sem filtros ou paginação.

    Args:
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[Book]: Lista com todos os livros cadastrados no sistema.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return list_all_books(db)


# GET /api/v1/books/search
@router.get(
    "/books/search",
    response_model=List[Book],
    responses={
        404: {"description": "Nenhum livro encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Buscar livros",
    description="Busca livros com base no título e/ou categoria."
)
def search_books_route(
    title: Optional[str] = None,
    category: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca livros por título e/ou categoria.

    Permite filtrar livros usando critérios de busca parcial (case-insensitive).
    Pode buscar apenas por título, apenas por categoria, ou por ambos simultaneamente.

    Args:
        title (Optional[str]): Título ou parte do título para filtrar. Se None, não filtra por título.
        category (Optional[str]): Categoria ou parte da categoria para filtrar. Se None, não filtra por categoria.
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[Book]: Lista de livros que correspondem aos critérios de busca.
                   Se ambos os parâmetros forem None, retorna todos os livros.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se nenhum livro corresponder aos critérios de busca
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return search_all_books(title, category, db)

# GET /api/v1/books/price-range
@router.get(
    "/books/price_range",
    response_model=List[Book],
    responses={
        404: {"description": "Nenhum livro encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Buscar livros por faixa de preço",
    description="Busca livros dentro de uma faixa de preço especificada."
)
def search_books_by_price_range(
    min: Optional[float] = None,
    max: Optional[float] = None,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Busca livros por faixa de preço.

    Retorna todos os livros cujo preço está entre min (inclusivo) e max (inclusivo).
    Se max for None, retorna todos os livros com preço maior ou igual a min.
    Se min for None, retorna todos os livros com preço menor ou igual a max.

    Args:
        min (Optional[float]): Preço mínimo (inclusivo). Se None, não há limite inferior.
        max (Optional[float]): Preço máximo (inclusivo). Se None, não há limite superior.
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[Book]: Lista de livros que estão na faixa de preço especificada.
                   Se ambos os parâmetros forem None, retorna todos os livros.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se nenhum livro corresponder à faixa de preço especificada
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return search_books_with_price(min, max, db)


# GET /api/v1/books/{book_id}
@router.get(
    "/books/{book_id}",
    response_model=BookDetails,
    responses={
        404: {"description": "Livro não encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Informações do livro",
    description="Retorna informações sobre o livro selecionado."
)
def get_book_route(book_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtém detalhes completos de um livro pelo ID.

    Retorna informações detalhadas do livro, incluindo preços com/sem impostos,
    UPC, número de avaliações, score, etc.

    Args:
        book_id (int): ID único do livro a ser buscado.
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        BookDetails: Objeto com detalhes completos do livro, incluindo:
                    - Informações básicas (id, title, author, year)
                    - Informações comerciais (price_without_tax, price_with_tax, tax)
                    - Informações de avaliação (score, number_reviews)
                    - Informações do produto (product_type, upc, available)

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se o livro não for encontrado
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return get_book_details(book_id, db)
