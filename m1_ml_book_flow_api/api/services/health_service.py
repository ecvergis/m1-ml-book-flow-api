from fastapi import HTTPException, status
from ..repositories.health_repository import get_books_count
from m1_ml_book_flow_api.core.logger import get_logger, log_error

health_logger = get_logger("health_service")

def check_api_health():
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
