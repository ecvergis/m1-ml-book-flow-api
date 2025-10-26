# api/routes/categories.py
from fastapi import APIRouter, Depends
from typing import List
from ..services.categories_service import list_all_categories
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.errors import ErrorResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/categories",
    response_model=List[str],
    responses={
        404: {"description": "Nenhuma categoria encontrada", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Listar todas as categorias",
    description="Retorna uma lista de categorias cadastradas."
)
def get_categories(current_user: dict = Depends(get_current_user)):
    return list_all_categories()
