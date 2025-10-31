"""
Modelo Pydantic para livros mais bem avaliados.

Este modelo define a estrutura de dados para livros com melhor avaliação.
"""
from pydantic import BaseModel

class TopRatedBook(BaseModel):
    """
    Modelo de livro top avaliado.
    
    Este modelo é usado para retornar informações sobre os livros
    com melhores avaliações (top rated).
    
    Attributes:
        title (str): Título do livro
        rating (float): Avaliação em estrelas (geralmente de 1.0 a 5.0)
    """
    title: str
    rating: float
