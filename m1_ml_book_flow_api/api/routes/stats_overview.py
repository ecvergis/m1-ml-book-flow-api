"""
Módulo de rotas para endpoints de estatísticas gerais (overview).

Este módulo define as rotas da API relacionadas a estatísticas gerais dos livros,
incluindo preço médio e distribuição de avaliações.
"""
from fastapi import APIRouter, Depends
from ..models.StatsOverview import StatsOverview
from ..services.stats_overview_service import get_stats
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.security.security import get_current_user

# Router com dependência de autenticação em todas as rotas
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
    """
    Retorna estatísticas gerais dos livros do sistema.

    Calcula e retorna uma visão geral das estatísticas do sistema, incluindo:
    - Total de livros cadastrados
    - Preço médio de todos os livros
    - Distribuição de avaliações (quantidade de livros por cada rating)

    Args:
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        StatsOverview: Objeto com estatísticas gerais contendo:
                       - total_books: Número total de livros cadastrados
                       - middle_price: Preço médio dos livros
                       - distribution_ratings: Distribuição de avaliações.
                         Chave: valor da avaliação (int ou float), Valor: quantidade de livros.
                         Exemplo: {4.0: 150, 4.5: 200, 5.0: 100}

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return get_stats()
