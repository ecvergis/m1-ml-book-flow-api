from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from ..models.StatsOverview import StatsOverview
from ..services.stats_overview_service import get_stats
from ...core.errors import ErrorResponse
from m1_ml_book_flow_api.core.security.security import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

# GET /api/v1/stats/overview
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

def get_statistics(
    current_user: dict = Depends(get_current_user)
):
    try:
        stats = get_stats()
        if stats is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado"
            )
        return stats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar os dados: {str(e)}"
        )