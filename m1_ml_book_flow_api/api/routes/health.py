from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from ..services.health_service import check_health
from ..models.HealthResponse import HealthResponse
from m1_ml_book_flow_api.core.security.security import get_current_user
from fastapi.responses import JSONResponse
from ...core.errors import ErrorResponse

router = APIRouter()

# GET /api/v1/health
@router.get(
    "/health",
    response_model=HealthResponse,
responses={
        404: {"description": "Nenhum dado encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Health check da API",
    description="Verifica status da API e conectividade com os dados"
)

def health():
    try:
        total_books = check_health()
        if total_books == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado"
            )
        return HealthResponse(
            status="ok",
            total_books=total_books,
            message="API funcionando e dados acessíveis"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar os dados: {str(e)}"
        )




