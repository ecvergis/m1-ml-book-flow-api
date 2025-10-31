"""
Módulo de repositório para gerenciamento de livros.

Este módulo contém funções para buscar, listar e filtrar livros a partir de uma
base de dados em memória (mock). Serve como camada de acesso aos dados de livros.

Nota: Esta implementação usa dados mock. Em produção, estas funções devem ser
adaptadas para acessar o banco de dados PostgreSQL.
"""
from typing import List, Optional
from m1_ml_book_flow_api.api.models.Book import Book
from m1_ml_book_flow_api.api.models.BookDetails import BookDetails

# Base de dados mock de livros (usado para testes e desenvolvimento)
BOOKS_DB = [
    Book(id=1, title="Livro A", author="Autor A", year=2020, category="Ficção", price=29.9, rating=4.5, available=True, image="url_a"),
    Book(id=2, title="Livro B", author="Autor B", year=2021, category="Romance", price=35.5, rating=4.0, available=True, image="url_b"),
    Book(id=3, title="Livro C", author="Autor C", year=2022, category="Suspense", price=40.0, rating=4.8, available=False, image="url_c"),
]

# BOOKS_DB = []

# Dados detalhados mock de um livro específico
BOOK_DETAILS = {
    "id": 1,
    "title": "Livro A",
    "author": "Autor A",
    "year": 2025,
    "score": 3.5,
    "price_without_tax": 37.90,
    "price_with_tax": 39.90,
    "tax": 2.00,
    "product_type": "Livro",
    "upc": "hgrf232",
    "available": True,
    "number_reviews": 67
}

def list_books() -> List[Book]:
    """
    Lista todos os livros disponíveis.

    Returns:
        List[Book]: Lista com todos os livros cadastrados no sistema.
    """
    return BOOKS_DB

def search_books_by(title: Optional[str] = None, category: Optional[str] = None) -> List[Book]:
    """
    Busca livros por título e/ou categoria.

    A busca por título é feita de forma parcial (case-insensitive), ou seja,
    se o título fornecido estiver contido no título do livro, ele será retornado.
    O mesmo vale para a categoria.

    Args:
        title (Optional[str]): Título ou parte do título para filtrar. Se None, não filtra por título.
        category (Optional[str]): Categoria ou parte da categoria para filtrar. Se None, não filtra por categoria.

    Returns:
        List[Book]: Lista de livros que correspondem aos critérios de busca.
                   Se ambos os parâmetros forem None, retorna todos os livros.
    """
    results = BOOKS_DB
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if category:
        results = [book for book in results if category.lower() in book.category.lower()]
    return results

def search_books_by_range_price(min_price: float = 0.0, max_price: Optional[float] = None) -> List[Book]:
    """
    Busca livros por faixa de preço.

    Retorna todos os livros cujo preço está entre min_price (inclusivo) e max_price (inclusivo).
    Se max_price for None, retorna todos os livros com preço maior ou igual a min_price.

    Args:
        min_price (float): Preço mínimo (inclusivo). Padrão: 0.0
        max_price (Optional[float]): Preço máximo (inclusivo). Se None, não há limite superior.

    Returns:
        List[Book]: Lista de livros que estão na faixa de preço especificada.
    """
    results = []

    for book in BOOKS_DB:
        if book.price >= min_price:
            if max_price is None or book.price <= max_price:
                results.append(book)

    return results

def get_book_by_id(book_id: int):
    """
    Obtém detalhes completos de um livro pelo ID.

    Retorna informações detalhadas do livro, incluindo preços com/sem impostos,
    UPC, número de avaliações, etc.

    Args:
        book_id (int): ID único do livro a ser buscado.

    Returns:
        dict: Dicionário com detalhes completos do livro se encontrado, None caso contrário.
              Contém campos: id, title, author, year, score, price_without_tax,
              price_with_tax, tax, product_type, upc, available, number_reviews.
    """
    book = BOOK_DETAILS
    if book['id'] == book_id:
        return book
    return None