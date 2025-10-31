"""
Módulo de rotas para endpoints de Machine Learning.

Este módulo define as rotas da API relacionadas ao Machine Learning,
incluindo features, dados de treinamento e predições.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from ..services.ml_service import (
    get_ml_features,
    get_ml_training_data,
    process_ml_predictions
)
from ..models.MLFeatures import MLFeaturesResponse
from ..models.MLTrainingData import MLTrainingDataResponse
from ..models.MLPredictions import MLPredictionsResponse, PredictionRequest
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.core.errors import ErrorResponse
from m1_ml_book_flow_api.core.logger import Logger

# Router com dependência de autenticação em todas as rotas
router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

# GET /api/v1/ml/features
@router.get(
    "/ml/features",
    response_model=MLFeaturesResponse,
    responses={
        404: {"description": "Nenhuma feature encontrada", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Obter features para ML",
    description="Retorna dados formatados como features para uso em modelos de Machine Learning."
)
def get_features_route(current_user: dict = Depends(get_current_user)):
    """
    Obtém features processadas para Machine Learning.
    
    Este endpoint retorna os dados dos livros processados e transformados
    em features numéricas adequadas para algoritmos de machine learning.
    
    As features incluem:
    - Comprimento do título
    - Autor codificado numericamente
    - Ano normalizado
    - Categoria codificada
    - Preço normalizado
    - Rating normalizado
    - Flag de disponibilidade
    - Score de popularidade
    
    Args:
        current_user: Usuário autenticado (injetado pela dependência)
        
    Returns:
        MLFeaturesResponse: Features processadas dos livros
        
    Raises:
        HTTPException: Se ocorrer erro no processamento
    """
    try:
        Logger.info("Requisição de features ML recebida", 
                   extra={"event": "ml_features_request", "user_id": current_user.get("user_id")})
        
        result = get_ml_features()
        
        if result.total_records == 0:
            Logger.warning("Nenhuma feature encontrada")
            raise HTTPException(status_code=404, detail="Nenhuma feature encontrada")
        
        Logger.info(f"Features ML retornadas: {result.total_records} registros", 
                   extra={"event": "ml_features_response", "total_records": result.total_records})
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        Logger.error(f"Erro ao obter features ML: {str(e)}", 
                    extra={"event": "ml_features_error", "error": str(e)})
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# GET /api/v1/ml/training-data
@router.get(
    "/ml/training-data",
    response_model=MLTrainingDataResponse,
    responses={
        404: {"description": "Nenhum dado de treinamento encontrado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Obter dados de treinamento para ML",
    description="Retorna dataset formatado para treinamento de modelos de Machine Learning."
)
def get_training_data_route(current_user: dict = Depends(get_current_user)):
    """
    Obtém dados de treinamento para Machine Learning.
    
    Este endpoint retorna um dataset estruturado para treinamento de modelos,
    incluindo features e targets para diferentes tipos de predições:
    - Predição de rating
    - Predição de preço
    - Classificação de categoria
    - Score de popularidade
    
    O dataset inclui informações sobre:
    - Registros de treinamento com features e targets
    - Estatísticas do dataset
    - Sugestões de divisão train/test/validation
    - Mapeamentos e normalizações aplicadas
    
    Args:
        current_user: Usuário autenticado (injetado pela dependência)
        
    Returns:
        MLTrainingDataResponse: Dataset de treinamento estruturado
        
    Raises:
        HTTPException: Se ocorrer erro no processamento
    """
    try:
        Logger.info("Requisição de dados de treinamento ML recebida", 
                   extra={"event": "ml_training_request", "user_id": current_user.get("user_id")})
        
        result = get_ml_training_data()
        
        if result.total_records == 0:
            Logger.warning("Nenhum dado de treinamento encontrado")
            raise HTTPException(status_code=404, detail="Nenhum dado de treinamento encontrado")
        
        Logger.info(f"Dados de treinamento ML retornados: {result.total_records} registros", 
                   extra={"event": "ml_training_response", "total_records": result.total_records})
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        Logger.error(f"Erro ao obter dados de treinamento ML: {str(e)}", 
                    extra={"event": "ml_training_error", "error": str(e)})
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

# POST /api/v1/ml/predictions
@router.post(
    "/ml/predictions",
    response_model=MLPredictionsResponse,
    responses={
        400: {"description": "Dados de entrada inválidos", "model": ErrorResponse},
        422: {"description": "Tipo de modelo não suportado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Realizar predições ML",
    description="Endpoint para receber e processar predições usando modelos de Machine Learning."
)
def make_predictions_route(
    request: PredictionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Realiza predições usando modelos de Machine Learning.
    
    Este endpoint processa requisições de predição para diferentes tipos de modelos:
    
    **Tipos de modelo suportados:**
    - `rating`: Predição de avaliação de livros
    - `price`: Predição de preço de livros
    - `category`: Classificação de categoria de livros
    - `recommendation`: Sistema de recomendação de livros
    
    **Estrutura da requisição:**
    - `model_type`: Tipo do modelo a ser usado
    - `input_features`: Features de entrada para predição
    - `book_ids`: IDs de livros (opcional, para recomendações)
    - `user_preferences`: Preferências do usuário (opcional)
    - `prediction_params`: Parâmetros adicionais (opcional)
    
    **Resposta inclui:**
    - Lista de predições com valores e scores de confiança
    - Informações sobre o modelo usado
    - Tempo de execução
    - Metadados da predição
    
    Args:
        request: Dados da requisição de predição
        current_user: Usuário autenticado (injetado pela dependência)
        
    Returns:
        MLPredictionsResponse: Resultados das predições
        
    Raises:
        HTTPException: Se ocorrer erro no processamento ou tipo de modelo inválido
    """
    try:
        Logger.info(f"Requisição de predição ML recebida - Tipo: {request.model_type}", 
                   extra={"event": "ml_prediction_request", "model_type": request.model_type, 
                         "user_id": current_user.get("user_id")})
        
        supported_models = ["rating", "price", "category", "recommendation"]
        if request.model_type not in supported_models:
            Logger.warning(f"Tipo de modelo não suportado: {request.model_type}")
            raise HTTPException(
                status_code=422, 
                detail=f"Tipo de modelo não suportado. Tipos suportados: {supported_models}"
            )
        
        if not request.input_features:
            Logger.warning("Features de entrada não fornecidas")
            raise HTTPException(status_code=400, detail="Features de entrada são obrigatórias")
        
        result = process_ml_predictions(request)
        
        Logger.info(f"Predições ML concluídas: {result.total_predictions} resultados em {result.execution_time_ms}ms", 
                   extra={"event": "ml_prediction_response", "total_predictions": result.total_predictions, 
                         "execution_time_ms": result.execution_time_ms})
        
        return result
        
    except HTTPException:
        raise
    except ValueError as e:
        Logger.error(f"Erro de validação em predições ML: {str(e)}", 
                    extra={"event": "ml_prediction_validation_error", "error": str(e)})
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        Logger.error(f"Erro ao processar predições ML: {str(e)}", 
                    extra={"event": "ml_prediction_error", "error": str(e)})
        raise HTTPException(status_code=500, detail="Erro interno do servidor")