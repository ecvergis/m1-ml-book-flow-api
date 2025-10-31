"""
Módulo de serviço para estatísticas gerais (overview) dos livros.

Este módulo contém a lógica de negócio relacionada a estatísticas gerais dos livros,
incluindo preço médio e distribuição de avaliações. Funciona como camada intermediária
entre as rotas (controllers) e os repositórios (data access).
"""
from fastapi import HTTPException, status
from ..repositories.stats_overview_repository import get_stats_overview

def get_stats():
    """
    Retorna estatísticas gerais dos livros do sistema.

    Calcula e retorna uma visão geral das estatísticas do sistema, incluindo:
    - Total de livros cadastrados
    - Preço médio de todos os livros
    - Distribuição de avaliações (quantidade de livros por cada rating)

    Returns:
        StatsOverview: Objeto com estatísticas gerais contendo:
                       - total_books: Número total de livros cadastrados
                       - middle_price: Preço médio dos livros
                       - distribution_ratings: Distribuição de avaliações.
                         Chave: valor da avaliação (int ou float), Valor: quantidade de livros.
                         Exemplo: {4.0: 150, 4.5: 200, 5.0: 100}

    Raises:
        HTTPException 404: Se não houver livros cadastrados
        HTTPException 500: Se ocorrer erro interno do servidor ou ao acessar os dados
    """
    try:
        stats = get_stats_overview()
        if stats is None:
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
