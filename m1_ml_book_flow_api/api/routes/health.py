"""
Módulo de rotas para endpoints de health check.

Este módulo define as rotas da API relacionadas à verificação de saúde e
disponibilidade da aplicação.
"""
from fastapi import APIRouter
from ..services.health_service import check_api_health
from ..models.HealthResponse import HealthResponse
from m1_ml_book_flow_api.core.errors import ErrorResponse

# Router sem dependência de autenticação (endpoint público para monitoramento)
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
    """
    Verifica o status de saúde da API e conectividade com os dados.

    Este endpoint é usado para monitoramento e verificação de disponibilidade
    da aplicação. Retorna informações sobre o status da API e estatísticas básicas.

    Returns:
        HealthResponse: Objeto com informações de saúde da API contendo:
                       - status: Status da API (ex: "healthy", "unhealthy", "ok")
                       - total_books: Número total de livros no sistema (se disponível)
                       - message: Mensagem adicional sobre o status (ex: mensagens de erro ou aviso)

    Raises:
        HTTPException 404: Se não houver dados disponíveis
        HTTPException 500: Se ocorrer erro interno do servidor

    Note:
        Este endpoint não requer autenticação e pode ser usado por sistemas
        de monitoramento e health checks externos.
    """
    return check_api_health()
