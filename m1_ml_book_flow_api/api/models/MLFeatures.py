"""
Modelo Pydantic para features de Machine Learning.

Este modelo define a estrutura de dados das features formatadas para uso em modelos ML.
"""
from pydantic import BaseModel
from typing import List, Optional

class BookFeature(BaseModel):
    """
    Modelo de feature de livro para Machine Learning.
    
    Este modelo representa um livro com suas features processadas e normalizadas
    para uso em algoritmos de machine learning.
    
    Attributes:
        id (int): Identificador único do livro
        title_length (int): Comprimento do título em caracteres
        author_encoded (int): Autor codificado numericamente
        year_normalized (float): Ano normalizado (0-1)
        category_encoded (int): Categoria codificada numericamente
        price_normalized (float): Preço normalizado (0-1)
        rating_normalized (float): Rating normalizado (0-1)
        availability_flag (int): Flag de disponibilidade (0 ou 1)
        popularity_score (float): Score de popularidade calculado
    """
    id: int
    title_length: int
    author_encoded: int
    year_normalized: float
    category_encoded: int
    price_normalized: float
    rating_normalized: float
    availability_flag: int
    popularity_score: float

class MLFeaturesResponse(BaseModel):
    """
    Resposta do endpoint de features ML.
    
    Attributes:
        features (List[BookFeature]): Lista de features dos livros
        total_records (int): Total de registros retornados
        feature_info (dict): Informações sobre as features (encodings, normalizações)
    """
    features: List[BookFeature]
    total_records: int
    feature_info: dict