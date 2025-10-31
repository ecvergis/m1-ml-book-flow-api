"""
Módulo de repositório para estatísticas gerais (overview) dos livros.

Este módulo contém funções para calcular e retornar estatísticas gerais do sistema,
incluindo preço médio e distribuição de avaliações.
"""
from typing import Optional, Counter
from ..models.StatsOverview import StatsOverview
from ..repositories.books_repository import list_books

def get_stats_overview() -> Optional[StatsOverview]:
    """
    Calcula e retorna estatísticas gerais dos livros do sistema.

    Calcula:
    - Total de livros cadastrados
    - Preço médio de todos os livros
    - Distribuição de avaliações (quantidade de livros por cada rating)

    Returns:
        Optional[StatsOverview]: Objeto com estatísticas gerais se houver livros,
                                 None se não houver livros cadastrados.

    Exemplo de distribuição de ratings:
        {4.0: 150, 4.5: 200, 5.0: 100} significa:
        - 150 livros com rating 4.0
        - 200 livros com rating 4.5
        - 100 livros com rating 5.0
    """
    books = list_books()
    if len(books) == 0:
        return None
    else:
        # Calcula preço médio
        middle_price = sum(book.price for book in books) / len(books)
        
        # Extrai todos os ratings disponíveis e conta a distribuição
        ratings = [book.rating for book in books if getattr(book, "rating", None) is not None]
        distribution_ratings = dict(Counter(ratings))

        stats = StatsOverview(
            total_books=len(books),
            middle_price=middle_price,
            distribution_ratings=distribution_ratings
        )
    return stats