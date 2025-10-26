from typing import List, Dict, Union, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from starlette import status
from m1_ml_book_flow_api.api.services.top_rating_service import get_ratings
from m1_ml_book_flow_api.core.security.security import get_current_user

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

# GET /api/v1/books/top-rated
@router.get(
    "/books/top-rated",
    description="Retorna uma lista de livros com a maior nota",
    response_model=List[Dict[str, Union[str, float]]],
    responses={
        404: {"description": "Nenhum dado encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
)
def get_rating_books(
    numberItems: int = Query(
        10,
        alias="numberItems",
        ge=1,
        description="Quantidade máxima de livros retornados"
    ),
    current_user: dict = Depends(get_current_user)
):
    try:
        rats = get_ratings(numberItems)
        if not rats or len(rats) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum dado encontrado"
            )
        return rats
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao acessar os dados: {str(e)}"
        )