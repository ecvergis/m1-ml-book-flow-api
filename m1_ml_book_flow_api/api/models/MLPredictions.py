"""
Modelo Pydantic para predições de Machine Learning.

Este modelo define a estrutura de dados para requisições e respostas de predições ML.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union

class PredictionRequest(BaseModel):
    """
    Modelo de requisição para predições ML.
    
    Este modelo define os dados de entrada necessários para fazer predições
    usando modelos de machine learning treinados.
    
    Attributes:
        model_type (str): Tipo do modelo (rating, price, category, recommendation)
        input_features (Dict[str, Any]): Features de entrada para predição
        book_ids (Optional[List[int]]): IDs de livros para recomendação (opcional)
        user_preferences (Optional[Dict[str, Any]]): Preferências do usuário (opcional)
        prediction_params (Optional[Dict[str, Any]]): Parâmetros adicionais para predição
    """
    model_type: str
    input_features: Dict[str, Any]
    book_ids: Optional[List[int]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    prediction_params: Optional[Dict[str, Any]] = None

class PredictionResult(BaseModel):
    """
    Modelo de resultado individual de predição.
    
    Attributes:
        book_id (int): ID do livro
        prediction_value (Union[float, str, int]): Valor predito
        confidence_score (float): Score de confiança da predição (0-1)
        prediction_type (str): Tipo da predição realizada
    """
    book_id: int
    prediction_value: Union[float, str, int]
    confidence_score: float
    prediction_type: str

class MLPredictionsResponse(BaseModel):
    """
    Resposta do endpoint de predições ML.
    
    Attributes:
        predictions (List[PredictionResult]): Lista de predições realizadas
        model_info (Dict[str, Any]): Informações sobre o modelo usado
        execution_time_ms (float): Tempo de execução em milissegundos
        total_predictions (int): Total de predições realizadas
        metadata (Dict[str, Any]): Metadados adicionais da predição
    """
    predictions: List[PredictionResult]
    model_info: Dict[str, Any]
    execution_time_ms: float
    total_predictions: int
    metadata: Dict[str, Any]