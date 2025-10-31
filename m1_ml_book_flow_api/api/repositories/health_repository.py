"""
Módulo de repositório para informações de health check.

Este módulo contém funções para fornecer estatísticas básicas utilizadas
no endpoint de health check da API.
"""
from ..repositories.books_repository import list_books

def get_books_count() -> int:
    """
    Obtém o número total de livros cadastrados no sistema.

    Esta função é usada pelo endpoint de health check para verificar se há
    dados disponíveis na aplicação.

    Returns:
        int: Número total de livros cadastrados. Retorna 0 se não houver livros.
    """
    books = list_books()
    return len(books)