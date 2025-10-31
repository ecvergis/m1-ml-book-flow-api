"""
Módulo de middlewares para requisições HTTP.

Este módulo contém middlewares que interceptam requisições HTTP para adicionar
funcionalidades transversais como logging, rastreamento de requisições, métricas
e extração de contexto de autenticação.
"""
import time
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from .logger import log_request, log_error, get_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging detalhado de requisições HTTP.

    Este middleware intercepta todas as requisições HTTP para registrar:
    - Início da requisição (método, caminho, query params, IP, user-agent)
    - Término da requisição (status code, duração, tamanho da resposta)
    - Erros durante o processamento
    - Geração de request_id único para rastreamento

    Attributes:
        logger: Logger configurado para este middleware
    """
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = get_logger("middleware")
        self.logger.setLevel(logging.DEBUG)

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        start_time = time.time()
        method = request.method
        path = request.url.path
        query_params = str(request.query_params) if request.query_params else None
        client_ip = request.client.host if request.client else None
        user_agent = request.headers.get("user-agent")

        request.state.request_id = request_id

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
            response = await call_next(request)
            duration = time.time() - start_time
            user_id = getattr(request.state, 'user_id', None)

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

            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            duration = time.time() - start_time

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

            raise e


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware para extração de contexto de autenticação.

    Este middleware extrai informações do token JWT do header Authorization
    e adiciona ao estado da requisição para uso posterior nos handlers.

    Adiciona ao request.state:
        - user_id: ID do usuário extraído do token (payload.sub)
        - username: Nome de usuário extraído do token (payload.username)
    """
    async def dispatch(self, request: Request, call_next):
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
                pass

        response = await call_next(request)
        return response

class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar métricas de desempenho às respostas.

    Este middleware calcula o tempo de processamento de cada requisição
    e adiciona um header customizado `X-Process-Time-ms` na resposta.

    O tempo é calculado em milissegundos e arredondado para 2 casas decimais.
    """
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = (time.time() - start_time) * 1000  # em ms

        response.headers["X-Process-Time-ms"] = str(round(duration, 2))
        return response