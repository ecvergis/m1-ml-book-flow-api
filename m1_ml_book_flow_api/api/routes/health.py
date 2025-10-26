from fastapi import APIRouter
from ..services.health_service import check_api_health
from ..models.HealthResponse import HealthResponse
from m1_ml_book_flow_api.core.errors import ErrorResponse

router = APIRouter()

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
    return check_api_health()
