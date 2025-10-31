"""
Módulo de repositório para estatísticas por categoria de livros.

Este módulo contém funções para calcular estatísticas agrupadas por categoria,
incluindo quantidade de livros e preço médio por categoria.
"""
from typing import Optional, List
from m1_ml_book_flow_api.api.models.StatsCategories import StatsCategories
from m1_ml_book_flow_api.api.services.books_service import list_books

def get_stats_categories() -> Optional[List[StatsCategories]]:
    """
    Calcula e retorna estatísticas agrupadas por categoria de livros.

    Para cada categoria, calcula:
    - Quantidade de livros na categoria
    - Preço médio dos livros da categoria

    Returns:
        Optional[List[StatsCategories]]: Lista de estatísticas por categoria se houver livros,
                                         None se não houver livros cadastrados.

    Cada item da lista contém:
        - category_name: Nome da categoria
        - quantity_books: Quantidade de livros nesta categoria
        - category_price: Preço médio dos livros da categoria (arredondado para 2 casas decimais)
    """
    books = list_books()
    if not books:
        return None

    # Agrupa livros por categoria e acumula preços
    category_data = {}

    for book in books:
        category = book.category
        if category not in category_data:
            category_data[category] = {"total_price": 0, "count": 0}
        category_data[category]["total_price"] += book.price
        category_data[category]["count"] += 1

    # Calcula estatísticas para cada categoria
    stats = []
    for category, data in category_data.items():
        avg_price = data["total_price"] / data["count"]
        stats.append(
            StatsCategories(
                category_name=category,
                quantity_books=data["count"],
                category_price=round(avg_price, 2)
            )
        )

    return stats
