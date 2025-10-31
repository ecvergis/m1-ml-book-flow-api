"""
Modelo Pydantic para dados de treinamento de Machine Learning.

Este modelo define a estrutura de dados do dataset formatado para treinamento de modelos ML.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TrainingRecord(BaseModel):
    """
    Modelo de registro de treinamento para Machine Learning.
    
    Este modelo representa um registro completo do dataset de treinamento,
    incluindo features e targets para diferentes tipos de modelos.
    
    Attributes:
        id (int): Identificador único do livro
        features (Dict[str, Any]): Dicionário com todas as features
        target_rating (float): Target para predição de rating
        target_price (float): Target para predição de preço
        target_category (str): Target para classificação de categoria
        target_popularity (float): Target para predição de popularidade
    """
    id: int
    features: Dict[str, Any]
    target_rating: float
    target_price: float
    target_category: str
    target_popularity: float

class MLTrainingDataResponse(BaseModel):
    """
    Resposta do endpoint de dados de treinamento ML.
    
    Attributes:
        training_data (List[TrainingRecord]): Lista de registros de treinamento
        total_records (int): Total de registros no dataset
        feature_columns (List[str]): Lista das colunas de features
        target_columns (List[str]): Lista das colunas de target
        dataset_info (Dict[str, Any]): Informações sobre o dataset (estatísticas, distribuições)
        split_info (Dict[str, Any]): Informações sobre divisão train/test/validation
    """
    training_data: List[TrainingRecord]
    total_records: int
    feature_columns: List[str]
    target_columns: List[str]
    dataset_info: Dict[str, Any]
    split_info: Dict[str, Any]