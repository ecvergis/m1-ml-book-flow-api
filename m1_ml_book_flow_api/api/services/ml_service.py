"""
Serviço de Machine Learning para processamento de dados e predições.

Este módulo contém a lógica de negócio para os endpoints de ML,
incluindo processamento de features, dados de treinamento e predições.
"""
import time
from typing import List, Dict, Any, Optional
from ..models.MLFeatures import MLFeaturesResponse, BookFeature
from ..models.MLTrainingData import MLTrainingDataResponse, TrainingRecord
from ..models.MLPredictions import MLPredictionsResponse, PredictionResult, PredictionRequest
from ..repositories.books_repository import list_books
from m1_ml_book_flow_api.core.logger import Logger

def get_ml_features() -> MLFeaturesResponse:
    """
    Obtém dados formatados como features para modelos ML.
    
    Processa os dados dos livros e os transforma em features numéricas
    adequadas para algoritmos de machine learning.
    
    Returns:
        MLFeaturesResponse: Features processadas dos livros
    """
    try:
        Logger.info("Iniciando processamento de features ML", extra={"event": "ml_features_start"})
        
        # Buscar todos os livros do banco
        books = list_books()
        
        if not books:
            Logger.warning("Nenhum livro encontrado para processamento de features")
            return MLFeaturesResponse(
                features=[],
                total_records=0,
                feature_info={}
            )
        
        # Processar features
        features = []
        authors = list(set([book.author for book in books if book.author]))
        categories = list(set([book.category for book in books if book.category]))
        
        # Criar mapeamentos para encoding
        author_mapping = {author: idx for idx, author in enumerate(authors)}
        category_mapping = {category: idx for idx, category in enumerate(categories)}
        
        # Normalização de valores
        years = [book.year for book in books if book.year]
        prices = [book.price for book in books if book.price]
        ratings = [book.rating for book in books if book.rating]
        
        min_year, max_year = min(years) if years else 2000, max(years) if years else 2024
        min_price, max_price = min(prices) if prices else 0, max(prices) if prices else 100
        min_rating, max_rating = min(ratings) if ratings else 0, max(ratings) if ratings else 5
        
        for book in books:
            # Calcular features
            title_length = len(book.title) if book.title else 0
            author_encoded = author_mapping.get(book.author, 0)
            year_normalized = (book.year - min_year) / (max_year - min_year) if max_year > min_year else 0.5
            category_encoded = category_mapping.get(book.category, 0)
            price_normalized = (book.price - min_price) / (max_price - min_price) if max_price > min_price else 0.5
            rating_normalized = (book.rating - min_rating) / (max_rating - min_rating) if max_rating > min_rating else 0.5
            availability_flag = 1 if book.available else 0
            
            # Score de popularidade simples (baseado em rating e disponibilidade)
            popularity_score = (rating_normalized * 0.7) + (availability_flag * 0.3)
            
            feature = BookFeature(
                id=book.id,
                title_length=title_length,
                author_encoded=author_encoded,
                year_normalized=round(year_normalized, 4),
                category_encoded=category_encoded,
                price_normalized=round(price_normalized, 4),
                rating_normalized=round(rating_normalized, 4),
                availability_flag=availability_flag,
                popularity_score=round(popularity_score, 4)
            )
            features.append(feature)
        
        feature_info = {
            "author_mapping": author_mapping,
            "category_mapping": category_mapping,
            "normalization_ranges": {
                "year": {"min": min_year, "max": max_year},
                "price": {"min": min_price, "max": max_price},
                "rating": {"min": min_rating, "max": max_rating}
            },
            "total_authors": len(authors),
            "total_categories": len(categories)
        }
        
        Logger.info(f"Features ML processadas com sucesso: {len(features)} registros", 
                   extra={"event": "ml_features_success", "total_records": len(features)})
        
        return MLFeaturesResponse(
            features=features,
            total_records=len(features),
            feature_info=feature_info
        )
        
    except Exception as e:
        Logger.error(f"Erro ao processar features ML: {str(e)}", 
                    extra={"event": "ml_features_error", "error": str(e)})
        raise

def get_ml_training_data() -> MLTrainingDataResponse:
    """
    Obtém dataset formatado para treinamento de modelos ML.
    
    Prepara os dados em formato adequado para treinamento,
    incluindo features e targets para diferentes tipos de modelos.
    
    Returns:
        MLTrainingDataResponse: Dataset de treinamento estruturado
    """
    try:
        Logger.info("Iniciando preparação de dados de treinamento ML", extra={"event": "ml_training_start"})
        
        # Buscar todos os livros do banco
        books = list_books()
        
        if not books:
            Logger.warning("Nenhum livro encontrado para dados de treinamento")
            return MLTrainingDataResponse(
                training_data=[],
                total_records=0,
                feature_columns=[],
                target_columns=[],
                dataset_info={},
                split_info={}
            )
        
        # Preparar dados de treinamento
        training_records = []
        
        for book in books:
            features = {
                "title_length": len(book.title) if book.title else 0,
                "author": book.author or "unknown",
                "year": book.year or 2000,
                "category": book.category or "unknown",
                "price": book.price or 0.0,
                "available": book.available
            }
            
            # Calcular popularidade baseada em rating e disponibilidade
            popularity = (book.rating * 0.8) + (1.0 if book.available else 0.0) * 0.2
            
            record = TrainingRecord(
                id=book.id,
                features=features,
                target_rating=book.rating or 0.0,
                target_price=book.price or 0.0,
                target_category=book.category or "unknown",
                target_popularity=round(popularity, 4)
            )
            training_records.append(record)
        
        # Informações do dataset
        feature_columns = ["title_length", "author", "year", "category", "price", "available"]
        target_columns = ["target_rating", "target_price", "target_category", "target_popularity"]
        
        # Estatísticas básicas
        ratings = [r.target_rating for r in training_records]
        prices = [r.target_price for r in training_records]
        
        dataset_info = {
            "total_records": len(training_records),
            "rating_stats": {
                "min": min(ratings) if ratings else 0,
                "max": max(ratings) if ratings else 0,
                "avg": sum(ratings) / len(ratings) if ratings else 0
            },
            "price_stats": {
                "min": min(prices) if prices else 0,
                "max": max(prices) if prices else 0,
                "avg": sum(prices) / len(prices) if prices else 0
            },
            "categories": list(set([r.target_category for r in training_records])),
            "availability_ratio": sum([1 for r in training_records if r.features["available"]]) / len(training_records)
        }
        
        # Informações de divisão (sugestão para train/test/validation)
        split_info = {
            "suggested_train_ratio": 0.7,
            "suggested_test_ratio": 0.2,
            "suggested_validation_ratio": 0.1,
            "total_for_train": int(len(training_records) * 0.7),
            "total_for_test": int(len(training_records) * 0.2),
            "total_for_validation": int(len(training_records) * 0.1)
        }
        
        Logger.info(f"Dados de treinamento ML preparados: {len(training_records)} registros", 
                   extra={"event": "ml_training_success", "total_records": len(training_records)})
        
        return MLTrainingDataResponse(
            training_data=training_records,
            total_records=len(training_records),
            feature_columns=feature_columns,
            target_columns=target_columns,
            dataset_info=dataset_info,
            split_info=split_info
        )
        
    except Exception as e:
        Logger.error(f"Erro ao preparar dados de treinamento ML: {str(e)}", 
                    extra={"event": "ml_training_error", "error": str(e)})
        raise

def process_ml_predictions(request: PredictionRequest) -> MLPredictionsResponse:
    """
    Processa predições usando modelos ML.
    
    Simula predições baseadas no tipo de modelo solicitado.
    Em uma implementação real, aqui seria carregado o modelo treinado.
    
    Args:
        request: Dados da requisição de predição
        
    Returns:
        MLPredictionsResponse: Resultados das predições
    """
    try:
        start_time = time.time()
        Logger.info(f"Iniciando predições ML - Tipo: {request.model_type}", 
                   extra={"event": "ml_prediction_start", "model_type": request.model_type})
        
        predictions = []
        
        # Simular predições baseadas no tipo de modelo
        if request.model_type == "rating":
            # Predição de rating baseada nas features
            predicted_rating = _predict_rating(request.input_features)
            predictions.append(PredictionResult(
                book_id=request.input_features.get("book_id", 0),
                prediction_value=predicted_rating,
                confidence_score=0.85,
                prediction_type="rating"
            ))
            
        elif request.model_type == "price":
            # Predição de preço
            predicted_price = _predict_price(request.input_features)
            predictions.append(PredictionResult(
                book_id=request.input_features.get("book_id", 0),
                prediction_value=predicted_price,
                confidence_score=0.78,
                prediction_type="price"
            ))
            
        elif request.model_type == "category":
            # Classificação de categoria
            predicted_category = _predict_category(request.input_features)
            predictions.append(PredictionResult(
                book_id=request.input_features.get("book_id", 0),
                prediction_value=predicted_category,
                confidence_score=0.92,
                prediction_type="category"
            ))
            
        elif request.model_type == "recommendation":
            # Sistema de recomendação
            recommendations = _get_recommendations(request.input_features, request.book_ids or [])
            predictions.extend(recommendations)
        
        else:
            raise ValueError(f"Tipo de modelo não suportado: {request.model_type}")
        
        execution_time = (time.time() - start_time) * 1000  # em milissegundos
        
        model_info = {
            "model_type": request.model_type,
            "model_version": "1.0.0",
            "last_trained": "2024-01-15",
            "algorithm": "Random Forest" if request.model_type in ["rating", "price"] else "Neural Network"
        }
        
        metadata = {
            "request_timestamp": time.time(),
            "input_features_count": len(request.input_features),
            "processing_status": "success"
        }
        
        Logger.info(f"Predições ML concluídas: {len(predictions)} resultados em {execution_time:.2f}ms", 
                   extra={"event": "ml_prediction_success", "total_predictions": len(predictions), 
                         "execution_time_ms": execution_time})
        
        return MLPredictionsResponse(
            predictions=predictions,
            model_info=model_info,
            execution_time_ms=round(execution_time, 2),
            total_predictions=len(predictions),
            metadata=metadata
        )
        
    except Exception as e:
        Logger.error(f"Erro ao processar predições ML: {str(e)}", 
                    extra={"event": "ml_prediction_error", "error": str(e)})
        raise

def _predict_rating(features: Dict[str, Any]) -> float:
    """Simula predição de rating baseada nas features."""
    # Lógica simplificada de predição
    base_rating = 3.0
    
    # Ajustes baseados nas features
    if features.get("year", 2000) > 2020:
        base_rating += 0.5
    if features.get("price", 0) > 50:
        base_rating += 0.3
    if "bestseller" in str(features.get("category", "")).lower():
        base_rating += 0.7
    
    return min(5.0, max(1.0, round(base_rating, 1)))

def _predict_price(features: Dict[str, Any]) -> float:
    """Simula predição de preço baseada nas features."""
    base_price = 25.0
    
    # Ajustes baseados nas features
    if features.get("year", 2000) > 2020:
        base_price += 10.0
    if features.get("title_length", 0) > 50:
        base_price += 5.0
    if "premium" in str(features.get("category", "")).lower():
        base_price += 15.0
    
    return round(base_price, 2)

def _predict_category(features: Dict[str, Any]) -> str:
    """Simula classificação de categoria baseada nas features."""
    # Lógica simplificada de classificação
    if features.get("year", 2000) > 2020:
        return "Ficção Contemporânea"
    elif features.get("price", 0) > 40:
        return "Literatura Premium"
    else:
        return "Ficção Geral"

def _get_recommendations(features: Dict[str, Any], book_ids: List[int]) -> List[PredictionResult]:
    """Simula sistema de recomendação."""
    recommendations = []
    
    # Simular recomendações baseadas nas features
    for i, book_id in enumerate(book_ids[:5]):  # Limitar a 5 recomendações
        score = 0.9 - (i * 0.1)  # Score decrescente
        recommendations.append(PredictionResult(
            book_id=book_id,
            prediction_value=score,
            confidence_score=score,
            prediction_type="recommendation_score"
        ))
    
    return recommendations