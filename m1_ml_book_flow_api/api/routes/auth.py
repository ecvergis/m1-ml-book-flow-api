from fastapi import APIRouter
from ..models.Auth import Auth
from ..models.RefreshToken import RefreshToken
from ..services.auth_service import login_service, refresh_token_service
from m1_ml_book_flow_api.core.errors import ErrorResponse

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
    return refresh_token_service(refresh_token)
