"""
Módulo de modelos para respostas de erro.

Este módulo define modelos Pydantic para padronizar respostas de erro da API,
seguindo um formato consistente para tratamento de erros.
"""
from pydantic import BaseModel, Field
from typing import Optional

class ErrorResponse(BaseModel):
    """
    Modelo de resposta padronizado para erros da API.

    Este modelo é usado em todos os handlers de exceção para garantir que
    as respostas de erro sigam um formato consistente e estruturado.

    Attributes:
        detail (str): Mensagem de erro descritiva para o usuário
        code (str): Código de status HTTP ou código de erro personalizado
        path (Optional[str]): Caminho da requisição que gerou o erro (se disponível)
    """
    detail: str
    code: str
    path: Optional[str] = None