"""
Módulo de serviço para health check da API.

Este módulo contém a lógica de negócio relacionada à verificação de saúde e
disponibilidade da aplicação, incluindo verificação de conectividade com os dados.
Funciona como camada intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from fastapi import HTTPException, status
from ..repositories.health_repository import get_books_count
from m1_ml_book_flow_api.core.logger import get_logger, log_error

health_logger = get_logger("health_service")

def check_api_health():
    """
    Verifica o status de saúde da API e conectividade com os dados.

    Verifica se a API está funcionando corretamente e se há dados disponíveis
    no sistema. Usado para monitoramento e verificação de disponibilidade.

    Returns:
        dict: Dicionário contendo:
            - status: Status da API (ex: "ok")
            - total_books: Número total de livros no sistema
            - message: Mensagem adicional sobre o status

    Raises:
        HTTPException 404: Se não houver dados disponíveis
        HTTPException 500: Se ocorrer erro interno do servidor ou ao acessar os dados
    """
    health_logger.info(
        "Checking API health",
        extra={"event": "health_check_start"}
    )
    
    try:
        total_books = get_books_count()
        if total_books == 0:
            health_logger.warning(
                "Health check failed - no data found",
                extra={
                    "event": "health_check_no_data",
                    "total_books": total_books,
                    "operation": "get_books_count"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado"
            )
        
        health_logger.info(
            "Health check successful",
            extra={
                "event": "health_check_success",
                "total_books": total_books,
                "status": "ok",
                "operation": "get_books_count"
            }
        )
        
        return {
            "status": "ok",
            "total_books": total_books,
            "message": "API funcionando e dados acessíveis"
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="check_api_health",
            event="health_check_error"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar os dados: {str(e)}"
        )
