from fastapi import HTTPException, status
from ..repositories.categories_repository import list_categories

def list_all_categories():
    categories = list_categories()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma categoria encontrada"
        )
    return categories
