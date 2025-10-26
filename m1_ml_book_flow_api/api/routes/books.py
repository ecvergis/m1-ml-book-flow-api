# api/routes/books.py
from fastapi import APIRouter, Depends
from typing import List, Optional
from ..services.books_service import (
    list_all_books,
    search_all_books,
    get_book_details,
    search_books_with_price
)
from m1_ml_book_flow_api.api.models.Book import Book
from m1_ml_book_flow_api.api.models.BookDetails import BookDetails
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.errors import ErrorResponse

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
def list_books(current_user: dict = Depends(get_current_user)):
    return list_all_books()


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
    current_user: dict = Depends(get_current_user)
):
    return search_all_books(title, category)

# GET /api/v1/books/price-range
@router.get(
    "/books/price_range",
    response_model=List[Book],
    responses={
        404: {"description": "Nenhum livro encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Buscar livros",
    description="Busca livros com base no título e/ou categoria."
)
def search_books_by_price_range(
    min: Optional[float] = None,
    max: Optional[float] = None,
    current_user: dict = Depends(get_current_user)
):
    return search_books_with_price(min, max)


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
def get_book_route(book_id: int, current_user: dict = Depends(get_current_user)):
    return get_book_details(book_id)
