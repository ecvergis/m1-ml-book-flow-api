"""
Módulo de rotas para endpoints de scraping.

Este módulo define as rotas da API relacionadas ao web scraping de livros.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from m1_ml_book_flow_api.core.database import get_db
from m1_ml_book_flow_api.core.security.security import get_current_user
from m1_ml_book_flow_api.api.services.scraping_trigger_service import trigger_scraping
from m1_ml_book_flow_api.core.errors import ErrorResponse

# Router com dependência de autenticação em todas as rotas
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
    Dispara o processo de web scraping de livros.
    
    Este endpoint executa o scraping completo do site books.toscrape.com,
    processando página por página e salvando os dados imediatamente no
    banco de dados PostgreSQL para evitar perda de dados.
    
    Args:
        current_user (dict): Usuário autenticado (obtido via token JWT)
        db (Session): Sessão do banco de dados (injetada automaticamente)
        
    Returns:
        Dict: Dicionário com resultados do scraping:
            - message: Mensagem de sucesso
            - scraped_count: Total de livros coletados
            - saved_count: Total de livros salvos
            - pages_processed: Número de páginas processadas
            
    Raises:
        HTTPException 401: Se o token de autenticação for inválido
        HTTPException 500: Se ocorrer erro durante o scraping ou salvamento
    """
    return trigger_scraping(db)

