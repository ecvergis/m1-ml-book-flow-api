"""
Módulo de repositório para livros mais bem avaliados (top rated).

Este módulo contém funções para buscar e retornar os livros com melhores avaliações,
ordenados por rating em ordem decrescente.
"""
from typing import List
from ..models.TopRatedBook import TopRatedBook
from ..services.books_service import list_books

def get_top_rating(number_items: int) -> List[TopRatedBook]:
    """
    Retorna os livros mais bem avaliados (top rated) do sistema.

    Ordena todos os livros por rating em ordem decrescente e retorna os N primeiros,
    onde N é especificado pelo parâmetro number_items.

    Args:
        number_items (int): Número máximo de livros a serem retornados no ranking.

    Returns:
        List[TopRatedBook]: Lista de livros ordenados por rating (do maior para o menor).
                           Retorna lista vazia se não houver livros cadastrados.
                           Se houver menos livros que number_items, retorna todos os disponíveis.

    Example:
        Se number_items=10, retorna os 10 livros com maior rating.
        Se houver apenas 5 livros, retorna esses 5 livros ordenados.
    """
    books = list_books()
    if not books:
        return []

    # Ordena livros por rating em ordem decrescente
    sorted_books = sorted(books, key=lambda b: b.rating, reverse=True)

    # Retorna apenas os N primeiros livros
    return [TopRatedBook(title=b.title, rating=b.rating) for b in sorted_books[:number_items]]
