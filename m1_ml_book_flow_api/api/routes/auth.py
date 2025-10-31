"""
Módulo de rotas para endpoints de autenticação.

Este módulo define as rotas da API relacionadas à autenticação de usuários,
incluindo login e renovação de tokens de acesso.
"""
from fastapi import APIRouter
from ..models.Auth import Auth
from ..models.RefreshToken import RefreshToken
from ..services.auth_service import login_service, refresh_token_service
from m1_ml_book_flow_api.core.errors import ErrorResponse

# Router sem dependência de autenticação (endpoints públicos)
router = APIRouter()

@router.post(
    "/login", 
    tags=["auth"],
    summary="Login do usuário",
    description="Realiza o login do usuário e retorna um token de acesso",
    responses={
        401: {"description": "Credenciais inválidas", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    }
)
def login(user: Auth):
    """
    Realiza o login do usuário e retorna tokens de acesso.

    Este endpoint valida as credenciais do usuário e, se válidas, retorna:
    - Access token: Token JWT para autenticação em endpoints protegidos
    - Refresh token: Token para renovação do access token quando expirado

    Args:
        user (Auth): Objeto Auth contendo username e password do usuário.

    Returns:
        dict: Dicionário contendo:
            - access_token: Token JWT de acesso
            - refresh_token: Token para renovação
            - token_type: Tipo do token (geralmente "bearer")

    Raises:
        HTTPException 401: Se as credenciais forem inválidas (username ou password incorretos)
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return login_service(user)

@router.post(
    "/refresh",
    tags=["auth"],
    summary="Renovar token de acesso",
    description="Renova o token de acesso usando um token válido existente",
    responses={
        401: {"description": "Token inválido ou expirado", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse},
    }
)
def refresh_token(refresh_token: RefreshToken):
    """
    Renova o token de acesso usando um refresh token válido.

    Este endpoint permite obter um novo access token usando um refresh token
    válido, sem precisar realizar login novamente. Isso é útil quando o
    access token expira.

    Args:
        refresh_token (RefreshToken): Objeto RefreshToken contendo o refresh_token válido.

    Returns:
        dict: Dicionário contendo:
            - access_token: Novo token JWT de acesso
            - token_type: Tipo do token (geralmente "bearer")

    Raises:
        HTTPException 401: Se o refresh token for inválido ou expirado
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    return refresh_token_service(refresh_token)
