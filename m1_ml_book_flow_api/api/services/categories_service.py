"""
Módulo de serviço para gerenciamento de categorias de livros.

Este módulo contém a lógica de negócio relacionada ao gerenciamento de categorias,
incluindo listagem de todas as categorias disponíveis. Funciona como camada
intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from fastapi import HTTPException, status
from ..repositories.categories_repository import list_categories
from m1_ml_book_flow_api.core.logger import get_logger, log_error

categories_logger = get_logger("categories_service")

def list_all_categories():
    """
    Lista todas as categorias únicas de livros disponíveis no sistema.

    Busca todas as categorias dos livros cadastrados, remove duplicatas e
    retorna uma lista ordenada alfabeticamente.

    Returns:
        List[str]: Lista ordenada alfabeticamente com todas as categorias únicas.
                   Retorna lista vazia se não houver livros ou categorias cadastradas.

    Raises:
        HTTPException 404: Se não houver categorias cadastradas
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    categories_logger.info(
        "Fetching all categories",
        extra={"event": "list_all_categories_start"}
    )
    
    try:
        categories = list_categories()
        if not categories:
            categories_logger.warning(
                "No categories found",
                extra={
                    "event": "list_all_categories_not_found",
                    "operation": "list_categories"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma categoria encontrada"
            )
        
        categories_logger.info(
            "Categories fetched successfully",
            extra={
                "event": "list_all_categories_success",
                "categories_count": len(categories),
                "operation": "list_categories"
            }
        )
        return categories
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="list_all_categories",
            event="list_all_categories_error"
        )
        raise
