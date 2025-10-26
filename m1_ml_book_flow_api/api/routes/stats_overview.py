from fastapi import APIRouter, Depends
from ..models.StatsOverview import StatsOverview
from ..services.stats_overview_service import get_stats
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.security.security import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/stats/overview",
    description="Retorna os dados estatísticos dos livros, de forma resumida",
    response_model=StatsOverview,
    responses={
        404: {"description": "Nenhum dado encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Resumo estatístico dos livros",
)
def get_statistics(current_user: dict = Depends(get_current_user)):
    return get_stats()
