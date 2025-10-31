"""
Modelo Pydantic para estatísticas gerais (overview) dos livros.

Este modelo define a estrutura de dados para estatísticas gerais do sistema.
"""
from typing import Dict, Union
from pydantic import BaseModel

class StatsOverview(BaseModel):
    """
    Modelo de estatísticas gerais dos livros.
    
    Este modelo é usado para retornar uma visão geral das estatísticas
    do sistema de livros, incluindo preço médio e distribuição de avaliações.
    
    Attributes:
        total_books (int): Número total de livros no sistema
        middle_price (float): Preço médio dos livros
        distribution_ratings (Dict[Union[int, float], int]): Distribuição de avaliações.
            Chave: valor da avaliação (int ou float), Valor: quantidade de livros com essa avaliação.
            Exemplo: {4.0: 150, 4.5: 200, 5.0: 100}
    """
    total_books: int
    middle_price: float
    distribution_ratings: Dict[Union[int, float], int]