"""
Modelo Pydantic para resposta do health check da API.

Este modelo define a estrutura de resposta do endpoint de verificação de saúde da API.
"""
from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    """
    Modelo de resposta do health check.
    
    Usado no endpoint de health check para retornar o status da API
    e informações sobre a disponibilidade dos dados.
    
    Attributes:
        status (str): Status da API (ex: "healthy", "unhealthy", "ok")
        total_books (int, optional): Número total de livros no sistema (se disponível)
        message (str, optional): Mensagem adicional sobre o status (ex: mensagens de erro ou aviso)
    """
    status: str
    total_books: Optional[int] = None
    message: Optional[str] = None