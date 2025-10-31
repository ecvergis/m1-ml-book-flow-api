"""
Módulo de serviço para estatísticas por categoria de livros.

Este módulo contém a lógica de negócio relacionada a estatísticas agrupadas por
categoria de livros, incluindo quantidade e preço médio por categoria. Funciona como
camada intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from fastapi import HTTPException, status
from ..repositories.stats_categories_repository import get_stats_categories

def get_stats():
    """
    Retorna estatísticas agrupadas por categoria de livros.

    Calcula e retorna estatísticas para cada categoria, incluindo:
    - Quantidade de livros em cada categoria
    - Preço médio dos livros de cada categoria

    Returns:
        List[StatsCategories]: Lista de estatísticas por categoria, onde cada item contém:
                               - category_name: Nome da categoria
                               - quantity_books: Quantidade de livros nesta categoria
                               - category_price: Preço médio dos livros da categoria
                                                 (arredondado para 2 casas decimais)
                               Retorna lista vazia se não houver livros cadastrados.

    Raises:
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor ou ao acessar os dados
    """
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
