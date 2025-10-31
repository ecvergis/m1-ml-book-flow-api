"""
Módulo de rotas para endpoints de estatísticas por categoria.

Este módulo define as rotas da API relacionadas a estatísticas agrupadas por
categoria de livros, incluindo quantidade e preço médio por categoria.
"""
from typing import List
from fastapi import APIRouter, Depends
from ..services.stats_categories_service import get_stats
from ..models.StatsCategories import StatsCategories
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.security.security import get_current_user

# Router com dependência de autenticação em todas as rotas
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
    """
    Retorna estatísticas agrupadas por categoria de livros.

    Calcula e retorna estatísticas para cada categoria, incluindo:
    - Quantidade de livros em cada categoria
    - Preço médio dos livros de cada categoria

    Args:
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[StatsCategories]: Lista de estatísticas por categoria, onde cada item contém:
                               - category_name: Nome da categoria
                               - quantity_books: Quantidade de livros nesta categoria
                               - category_price: Preço médio dos livros da categoria
                                                 (arredondado para 2 casas decimais)
                               Retorna lista vazia se não houver livros cadastrados.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return get_stats()
