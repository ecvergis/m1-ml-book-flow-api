"""
Modelo Pydantic para representação de livro na API.

Este modelo define a estrutura de dados de um livro retornado pelos endpoints da API.
"""
from pydantic import BaseModel

class Book(BaseModel):
    """
    Modelo de livro básico retornado pela API.
    
    Este modelo é usado para listar livros e respostas de busca.
    
    Attributes:
        id (int): Identificador único do livro
        title (str): Título do livro
        author (str): Nome do autor
        year (int): Ano de publicação
        category (str): Categoria/genêro do livro
        price (float): Preço do livro
        rating (float): Avaliação em estrelas (geralmente de 1.0 a 5.0)
        available (bool): Indica se o livro está disponível em estoque
        image (str): URL da imagem da capa do livro
    """
    id: int
    title: str
    author: str
    year: int
    category: str
    price: float
    rating: float
    available: bool
    image: str