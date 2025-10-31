"""
Módulo de repositório para gerenciamento de categorias de livros.

Este módulo contém funções para extrair e listar categorias únicas a partir
dos livros cadastrados no sistema.
"""
from m1_ml_book_flow_api.api.repositories.books_repository import list_books

def list_categories():
    """
    Lista todas as categorias únicas de livros disponíveis no sistema.

    Extrai todas as categorias dos livros cadastrados, remove duplicatas e
    retorna uma lista ordenada alfabeticamente.

    Returns:
        List[str]: Lista ordenada alfabeticamente com todas as categorias únicas.
                   Retorna lista vazia se não houver livros ou categorias cadastradas.
    """
    categories = set()
    books = list_books()
    for book in books:
        if getattr(book, "category", None):
            categories.add(book.category)
    return sorted(list(categories))