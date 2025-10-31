"""
Módulo de rotas para endpoints de livros mais bem avaliados (top rated).

Este módulo define as rotas da API relacionadas aos livros com melhores
avaliações, ordenados por rating em ordem decrescente.
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from ..models.TopRatedBook import TopRatedBook
from ..services.top_rating_service import get_top_rating_books_service
from m1_ml_book_flow_api.core.security.security import get_current_user

# Router com dependência de autenticação em todas as rotas
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/books/top-rated",
    description="Retorna uma lista de livros com a maior nota",
    response_model=List[TopRatedBook],
    responses={
        404: {"description": "Nenhum dado encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
    summary="Livros com as melhores avaliações"
)
def get_rating_books(
    number_items: int = Query(
        10,
        ge=1,
        description="Quantidade máxima de livros retornados"),
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os livros mais bem avaliados (top rated) do sistema.

    Ordena todos os livros por rating em ordem decrescente e retorna os N primeiros,
    onde N é especificado pelo parâmetro number_items.

    Args:
        number_items (int): Número máximo de livros a serem retornados no ranking.
                          Valor mínimo: 1. Padrão: 10.
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[TopRatedBook]: Lista de livros ordenados por rating (do maior para o menor),
                           contendo apenas título e rating.
                           Retorna lista vazia se não houver livros cadastrados.
                           Se houver menos livros que number_items, retorna todos os disponíveis.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor

    Example:
        Se number_items=10, retorna os 10 livros com maior rating.
        Se houver apenas 5 livros, retorna esses 5 livros ordenados.
    """
    return get_top_rating_books_service(number_items)
