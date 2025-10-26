import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .logger import log_request, log_error, get_logger
import json


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para capturar e logar todas as requisições HTTP
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger("middleware")
        self.logger.setLevel(logging.DEBUG)

    async def dispatch(self, request: Request, call_next):
        # Gerar ID único para a requisição
        request_id = str(uuid.uuid4())

        # Capturar dados da requisição
        start_time = time.time()
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else None
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        # Adicionar request_id ao state para uso em outros lugares
        request.state.request_id = request_id

        # Log de início da requisição
        self.logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "http_method": method,
                "http_path": path,
                "query_params": query_params,
                "client_ip": client_ip,
                "user_agent": user_agent,
                "event": "request_start"
            }
        )

        try:
            # Processar a requisição
            response = await call_next(request)

            # Calcular duração
            duration = time.time() - start_time

            # Extrair user_id se disponível (do token JWT)
            user_id = getattr(request.state, 'user_id', None)

            # Log da resposta
            log_request(
                method=method,
                path=path,
                status_code=response.status_code,
                duration=duration,
                user_id=user_id,
                request_id=request_id,
                client_ip=client_ip,
                query_params=query_params,
                response_size=response.headers.get("content-length"),
                event="request_complete"
            )

            # Adicionar headers de correlação
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            # Calcular duração mesmo em caso de erro
            duration = time.time() - start_time

            # Log do erro
            log_error(
                error=e,
                context="HTTP Request",
                request_id=request_id,
                http_method=method,
                http_path=path,
                duration_ms=round(duration * 1000, 2),
                client_ip=client_ip,
                event="request_error"
            )

            # Re-raise a exceção para que o FastAPI possa tratá-la
            raise e


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar contexto de requisição
    """

    async def dispatch(self, request: Request, call_next):
        # Extrair informações do usuário do token JWT se disponível
        authorization = request.headers.get("authorization")
        if authorization and authorization.startswith("Bearer "):
            try:
                from ..core.security.security import decode_access_token
                token = authorization.split(" ")[1]
                payload = decode_access_token(token)
                if payload:
                    request.state.user_id = payload.get("sub")
                    request.state.username = payload.get("username")
            except Exception:
                # Se não conseguir decodificar o token, continua sem user_id
                pass

        response = await call_next(request)
        return response