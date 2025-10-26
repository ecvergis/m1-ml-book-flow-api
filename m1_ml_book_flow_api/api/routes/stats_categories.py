from typing import List
from fastapi import APIRouter, Depends
from ..services.stats_categories_service import get_stats
from ..models.StatsCategories import StatsCategories
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.security.security import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/stats/categories",
    description="Retorna os dados estatísticos das categorias, de forma resumida",
    response_model=List[StatsCategories],
    responses={
        404: {"description": "Nenhum dado encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Resumo estatístico das categorias",
)
def get_statistics(current_user: dict = Depends(get_current_user)):
    return get_stats()
