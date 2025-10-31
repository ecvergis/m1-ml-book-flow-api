"""
Módulo utilitário para criação de tokens JWT de teste.

Este módulo fornece funções para criar tokens JWT simples para testes,
usando uma chave secreta fixa. Não deve ser usado em produção.

Nota: Este módulo é destinado apenas para testes. Use security.py para produção.
"""
from datetime import datetime, timedelta
import jwt

# Chave secreta fixa para testes (NÃO usar em produção)
SECRET_KEY = "minha_chave_secreta_teste"
ALGORITHM = "HS256"

def create_test_token(user_id: str, expires_delta: timedelta = None):
    """
    Cria um token JWT de teste para um usuário.

    Esta função gera um token JWT simples com o user_id especificado,
    útil para testes e desenvolvimento.

    Args:
        user_id (str): ID do usuário para incluir no token (payload.sub)
        expires_delta (timedelta, optional): Tempo até a expiração do token.
                                           Se None, usa 30 minutos como padrão.

    Returns:
        str: Token JWT codificado como string

    Note:
        Esta função é destinada apenas para testes. Use create_access_token
        do módulo security.py para produção.
    """
    to_encode = {"sub": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
