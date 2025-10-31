"""
Modelo Pydantic para renovação de token de acesso.

Este modelo define a estrutura de dados para requisições de refresh token.
"""
from pydantic.v1 import BaseModel

class RefreshToken(BaseModel):
    """
    Modelo para requisição de renovação de token de acesso.
    
    Usado no endpoint de refresh token para obter um novo access token
    usando um refresh token válido.
    
    Attributes:
        refresh_token (str): Token de atualização (refresh token) válido
    """
    refresh_token: str