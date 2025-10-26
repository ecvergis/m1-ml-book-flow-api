from typing import List, Dict, Union, Any
from fastapi import APIRouter, Depends, Query
from ..models.TopRatedBook import TopRatedBook
from ..services.top_rating_service import get_top_rating_books_service
from m1_ml_book_flow_api.core.security.security import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/books/top-rated",
    description="Retorna uma lista de livros com a maior nota",
    response_model=List[TopRatedBook],
    responses={
        404: {"description": "Nenhum dado encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
    summary="Livros com as melhores avaliações"
)
def get_rating_books(
    number_items: int = Query(
        10,
        ge=1,
        description="Quantidade máxima de livros retornados"),
    current_user: dict = Depends(get_current_user)
):
    print("number_items recebido:", number_items)
    return get_top_rating_books_service(number_items)
