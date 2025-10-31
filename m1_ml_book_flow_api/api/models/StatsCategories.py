"""
Modelo Pydantic para estatísticas por categoria.

Este modelo define a estrutura de dados para estatísticas de livros por categoria.
"""
from pydantic import BaseModel

class StatsCategories(BaseModel):
    """
    Modelo de estatísticas por categoria de livro.
    
    Este modelo representa as estatísticas de uma categoria específica,
    incluindo quantidade de livros e preço relacionado à categoria.
    
    Attributes:
        category_name (str): Nome da categoria (ex: "Romance", "Ficção Científica")
        quantity_books (int): Quantidade de livros nesta categoria
        category_price (float): Preço total ou preço médio dos livros da categoria
    """
    category_name: str
    quantity_books: int
    category_price: float