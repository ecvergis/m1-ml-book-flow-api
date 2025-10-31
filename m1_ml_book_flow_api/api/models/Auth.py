"""
Modelo Pydantic para autenticação de usuários.

Este modelo define a estrutura de dados para requisições de login.
"""
from pydantic.v1 import BaseModel

class Auth(BaseModel):
    """
    Modelo de credenciais de autenticação.
    
    Usado no endpoint de login para validar credenciais do usuário.
    
    Attributes:
        username (str): Nome de usuário para autenticação
        password (str): Senha do usuário
    """
    username: str
    password: str