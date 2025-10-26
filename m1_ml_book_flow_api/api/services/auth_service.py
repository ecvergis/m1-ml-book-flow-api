from ..models.Auth import Auth
from ..models.RefreshToken import RefreshToken
from ..repositories.auth_repository import login_user
from m1_ml_book_flow_api.core.security.security import create_access_token, create_refresh_token, decode_refresh_token
from m1_ml_book_flow_api.core.logger import log_auth_event, log_error, get_logger
from fastapi import HTTPException, status

auth_logger = get_logger("auth_service")

def login_service(user: Auth):
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
