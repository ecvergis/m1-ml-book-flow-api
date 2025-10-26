from fastapi import HTTPException, status
from ..repositories.categories_repository import list_categories
from m1_ml_book_flow_api.core.logger import get_logger, log_error

categories_logger = get_logger("categories_service")

def list_all_categories():
    categories_logger.info(
        "Fetching all categories",
        extra={"event": "list_all_categories_start"}
    )
    
    try:
        categories = list_categories()
        if not categories:
            categories_logger.warning(
                "No categories found",
                extra={
                    "event": "list_all_categories_not_found",
                    "operation": "list_categories"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhuma categoria encontrada"
            )
        
        categories_logger.info(
            "Categories fetched successfully",
            extra={
                "event": "list_all_categories_success",
                "categories_count": len(categories),
                "operation": "list_categories"
            }
        )
        return categories
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="list_all_categories",
            event="list_all_categories_error"
        )
        raise
