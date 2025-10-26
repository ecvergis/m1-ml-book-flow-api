from fastapi import HTTPException, status
from ..repositories.stats_overview_repository import get_stats_overview

def get_stats():
    try:
        stats = get_stats_overview()
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
