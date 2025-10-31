"""
Módulo de rotas para endpoints de categorias de livros.

Este módulo define as rotas da API relacionadas ao gerenciamento de categorias,
incluindo listagem de todas as categorias disponíveis.
"""
# api/routes/categories.py
from fastapi import APIRouter, Depends
from typing import List
from ..services.categories_service import list_all_categories
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.errors import ErrorResponse

# Router com dependência de autenticação em todas as rotas
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.get(
    "/categories",
    response_model=List[str],
    responses={
        404: {"description": "Nenhuma categoria encontrada", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Listar todas as categorias",
    description="Retorna uma lista de categorias cadastradas."
)
def get_categories(current_user: dict = Depends(get_current_user)):
    """
    Lista todas as categorias únicas de livros disponíveis no sistema.

    Este endpoint extrai todas as categorias dos livros cadastrados, remove
    duplicatas e retorna uma lista ordenada alfabeticamente.

    Args:
        current_user (dict): Usuário autenticado (obtido via token JWT)

    Returns:
        List[str]: Lista ordenada alfabeticamente com todas as categorias únicas.
                   Retorna lista vazia se não houver livros ou categorias cadastradas.

    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 404: Se não houver categorias cadastradas
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return list_all_categories()
