"""
Módulo de segurança para autenticação JWT.

Este módulo fornece funções para criação, validação e decodificação de tokens JWT
(JSON Web Tokens) para autenticação de usuários. Inclui suporte para access tokens
e refresh tokens com diferentes tempos de expiração.
"""
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os

# Configurações de segurança
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")  # Chave secreta para assinar tokens
ALGORITHM = "HS256"  # Algoritmo de criptografia para tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Tempo de expiração do access token em minutos
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Tempo de expiração do refresh token em dias

# Instância HTTPBearer para validação automática de tokens
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um access token JWT.

    Gera um token JWT de acesso com o payload especificado e tempo de expiração.
    O token inclui um campo "type": "access" para diferenciá-lo de refresh tokens.

    Args:
        data (dict): Dados a serem incluídos no payload do token (ex: {"sub": "user_id"})
        expires_delta (Optional[timedelta]): Tempo até a expiração do token.
                                          Se None, usa ACCESS_TOKEN_EXPIRE_MINUTES como padrão.

    Returns:
        str: Token JWT codificado como string

    Example:
        token = create_access_token({"sub": "user123"})
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Cria um refresh token JWT.

    Gera um token JWT de renovação com o payload especificado e tempo de expiração.
    O token inclui um campo "type": "refresh" para diferenciá-lo de access tokens.
    Refresh tokens têm um tempo de expiração maior que access tokens.

    Args:
        data (dict): Dados a serem incluídos no payload do token (ex: {"sub": "user_id"})
        expires_delta (Optional[timedelta]): Tempo até a expiração do token.
                                          Se None, usa REFRESH_TOKEN_EXPIRE_DAYS como padrão.

    Returns:
        str: Token JWT codificado como string

    Example:
        token = create_refresh_token({"sub": "user123"})
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodifica e valida um access token JWT.

    Valida o token JWT, verifica se não está expirado e se é do tipo "access".
    Retorna o payload decodificado se válido.

    Args:
        token (str): Token JWT a ser decodificado

    Returns:
        dict: Payload decodificado do token contendo os dados (ex: {"sub": "user_id", "exp": 123456})

    Raises:
        HTTPException 401: Se o token estiver expirado, for inválido ou não for do tipo "access"
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo de token inválido")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

def decode_refresh_token(token: str):
    """
    Decodifica e valida um refresh token JWT.

    Valida o token JWT, verifica se não está expirado e se é do tipo "refresh".
    Retorna o payload decodificado se válido.

    Args:
        token (str): Token JWT a ser decodificado

    Returns:
        dict: Payload decodificado do token contendo os dados (ex: {"sub": "user_id", "exp": 123456})

    Raises:
        HTTPException 401: Se o token estiver expirado, for inválido ou não for do tipo "refresh"
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo de token inválido")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency do FastAPI para obter o usuário atual autenticado.

    Extrai o token JWT do header Authorization e valida/decodifica para
    retornar o payload com informações do usuário autenticado.

    Esta função pode ser usada como dependency em rotas protegidas para
    garantir que apenas usuários autenticados possam acessar o endpoint.

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciais extraídas do header Authorization

    Returns:
        dict: Payload decodificado do token contendo informações do usuário (ex: {"sub": "user_id"})

    Raises:
        HTTPException 401: Se o token estiver ausente, expirado ou inválido

    Example:
        @router.get("/protected")
        def protected_route(current_user: dict = Depends(get_current_user)):
            user_id = current_user.get("sub")
            return {"message": f"Olá, usuário {user_id}"}
    """
    token = credentials.credentials
    return decode_access_token(token)
