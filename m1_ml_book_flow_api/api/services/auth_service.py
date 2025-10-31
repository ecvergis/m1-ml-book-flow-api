"""
Módulo de serviço para autenticação de usuários.

Este módulo contém a lógica de negócio relacionada à autenticação de usuários,
incluindo validação de credenciais, geração de tokens JWT e renovação de tokens.
Funciona como camada intermediária entre as rotas (controllers) e os repositórios (data access).
"""
from ..models.Auth import Auth
from ..models.RefreshToken import RefreshToken
from ..repositories.auth_repository import login_user
from m1_ml_book_flow_api.core.security.security import create_access_token, create_refresh_token, decode_refresh_token
from m1_ml_book_flow_api.core.logger import log_auth_event, log_error, get_logger
from fastapi import HTTPException, status

auth_logger = get_logger("auth_service")

def login_service(user: Auth):
    """
    Realiza o login do usuário e retorna tokens de acesso.

    Valida as credenciais do usuário e, se válidas, gera e retorna:
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
    auth_logger.info(
        "Login attempt",
        extra={
            "username": user.username,
            "event": "login_attempt"
        }
    )
    
    try:
        userLogged = login_user(user)
        if not userLogged:
            log_auth_event(
                event_type="login_failed",
                success=False,
                username=user.username,
                reason="invalid_credentials"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas"
            )

        access_token = create_access_token({"sub": userLogged.username})
        refresh_token = create_refresh_token({"sub": userLogged.username})
        
        log_auth_event(
            event_type="login_success",
            user_id=userLogged.username,
            success=True,
            username=userLogged.username
        )
        
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="login_service",
            username=user.username,
            event="login_error"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

def refresh_token_service(refresh_token_data: RefreshToken):
    """
    Renova o token de acesso usando um refresh token válido.

    Valida o refresh token fornecido e, se válido, gera um novo access token
    sem precisar realizar login novamente. Isso é útil quando o access token expira.

    Args:
        refresh_token_data (RefreshToken): Objeto RefreshToken contendo o refresh_token válido.

    Returns:
        dict: Dicionário contendo:
            - access_token: Novo token JWT de acesso
            - token_type: Tipo do token (geralmente "bearer")

    Raises:
        HTTPException 401: Se o refresh token for inválido ou expirado
        HTTPException 500: Se ocorrer erro interno do servidor
    """
    auth_logger.info(
        "Refresh token attempt",
        extra={
            "event": "refresh_attempt"
        }
    )
    
    try:
        payload = decode_refresh_token(refresh_token_data.refresh_token)
        username = payload.get("sub")
        
        if not username:
            log_auth_event(
                event_type="refresh_failed",
                success=False,
                reason="invalid_token"
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        new_access_token = create_access_token({"sub": username})
        
        log_auth_event(
            event_type="refresh_success",
            user_id=username,
            success=True,
            username=username
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(
            error=e,
            context="refresh_token_service",
            event="refresh_error"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao processar refresh token"
        )
