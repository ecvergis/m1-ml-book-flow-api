from fastapi import HTTPException, status
from ..repositories.health_repository import get_books_count

def check_api_health():
    try:
        total_books = get_books_count()
        if total_books == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado"
            )
        return {
            "status": "ok",
            "total_books": total_books,
            "message": "API funcionando e dados acessíveis"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar os dados: {str(e)}"
        )
