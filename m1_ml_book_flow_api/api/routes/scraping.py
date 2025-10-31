from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from m1_ml_book_flow_api.core.database import get_db
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.api.services.scraping_trigger_service import trigger_scraping
from m1_ml_book_flow_api.core.errors import ErrorResponse

router = APIRouter(
    dependencies=[Depends(get_current_user)]
)

@router.post(
    "/scraping/trigger",
    response_model=Dict,
    responses={
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    },
    summary="Disparar scraping de livros",
    description="Executa web scraping do site books.toscrape.com e armazena os dados no banco de dados PostgreSQL"
)
def trigger_scraping_route(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Trigger web scraping process.
    Requires authentication.
    """
    return trigger_scraping(db)

