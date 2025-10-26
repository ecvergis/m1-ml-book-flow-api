from fastapi import HTTPException, status
from ..repositories.stats_categories_repository import get_stats_categories

def get_stats():
    try:
        stats = get_stats_categories()
        if stats is None or len(stats) == 0:
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
