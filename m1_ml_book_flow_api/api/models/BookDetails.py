"""
Modelo Pydantic para detalhes completos de um livro.

Este modelo contém informações detalhadas de um livro específico,
incluindo informações fiscais e comerciais adicionais.
"""
from pydantic import BaseModel

class BookDetails(BaseModel):
    """
    Modelo com detalhes completos de um livro.
    
    Este modelo é usado para retornar informações detalhadas de um livro específico,
    incluindo informações de preço com/sem impostos e estatísticas de avaliações.
    
    Attributes:
        id (int): Identificador único do livro
        title (str): Título do livro
        author (str): Nome do autor
        year (int): Ano de publicação
        score (float): Pontuação/avaliação do livro
        price_without_tax (float): Preço sem impostos
        price_with_tax (float): Preço com impostos
        tax (float): Valor do imposto
        product_type (str): Tipo de produto (ex: "Livro", "E-book")
        upc (str): Código UPC (Universal Product Code) do produto
        available (bool): Indica se o livro está disponível em estoque
        number_reviews (int): Número total de avaliações/resenhas
    """
    id: int
    title: str
    author: str
    year: int
    score: float
    price_without_tax: float
    price_with_tax: float
    tax: float
    product_type: str
    upc: str
    available: bool
    number_reviews: int

