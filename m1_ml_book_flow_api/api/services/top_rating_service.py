from typing import List
from ..models.Book import Book
from ..repositories.top_rating_repository import get_top_rating
from m1_ml_book_flow_api.core.logger import get_logger, log_error
from fastapi import HTTPException, status

top_rating_logger = get_logger("top_rating_service")

def get_top_rating_books_service(limit: int = 10) -> List[Book]:
    top_rating_logger.info(
        "Fetching top rating books",
        extra={
            "event": "get_top_rating_books_start",
            "limit": limit
        }
    )
    
    try:
        ratings = get_top_rating(limit)
        
        if not ratings:
            top_rating_logger.warning(
                "No top rating books found",
                extra={
                    "event": "get_top_rating_books_not_found",
                    "limit": limit,
                    "operation": "get_top_rating_books"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum livro com avaliação encontrado"
            )
        
        top_rating_logger.info(
            "Top rating books fetched successfully",
            extra={
                "event": "get_top_rating_books_success",
                "books_count": len(ratings),
                "limit": limit,
                "operation": "get_top_rating_books"
            }
        )
        return ratings
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="get_top_rating_books_service",
            limit=limit,
            event="get_top_rating_books_error"
        )
        raise
