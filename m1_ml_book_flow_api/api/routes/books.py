from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..services.books_service import get_all_books
from m1_ml_book_flow_api.api.models.book import Book
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.exceptions import NotFoundException

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
    books = get_all_books()
    return books