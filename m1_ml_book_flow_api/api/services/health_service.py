from fastapi import HTTPException, status
from ..repositories.health_repository import get_books_count
from ..models.HealthResponse import HealthResponse

def check_health() -> int:
    return get_books_count()
