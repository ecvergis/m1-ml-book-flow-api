"""
Módulo de handlers para tratamento de exceções.

Este módulo contém handlers personalizados para tratamento centralizado de
exceções na API, garantindo respostas padronizadas para todos os tipos de erro.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from m1_ml_book_flow_api.core.errors import ErrorResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler para exceções HTTP genéricas.

    Trata exceções HTTP (404, 403, 401, etc.) e retorna uma resposta JSON
    padronizada com informações sobre o erro.

    Args:
        request (Request): Objeto da requisição FastAPI
        exc (StarletteHTTPException): Exceção HTTP lançada

    Returns:
        JSONResponse: Resposta JSON padronizada contendo:
                      - detail: Mensagem de erro
                      - code: Código de status HTTP
                      - path: Caminho da requisição que gerou o erro
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail or "Erro HTTP genérico",
            code=str(exc.status_code),
            path=str(request.url),
        ).model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler para exceções de validação de dados.

    Trata erros de validação do Pydantic quando os dados da requisição não
    atendem aos requisitos definidos nos modelos.

    Args:
        request (Request): Objeto da requisição FastAPI
        exc (RequestValidationError): Exceção de validação lançada

    Returns:
        JSONResponse: Resposta JSON padronizada contendo:
                      - detail: Mensagem de erro de validação
                      - code: Código de status HTTP (422)
                      - path: Caminho da requisição que gerou o erro
    """
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            detail="Erro de validação nos dados enviados",
            code="422",
            path=str(request.url),
        ).model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handler genérico para exceções não tratadas.

    Trata qualquer exceção não capturada pelos outros handlers, garantindo
    que sempre haja uma resposta estruturada, mesmo em caso de erros inesperados.

    Args:
        request (Request): Objeto da requisição FastAPI
        exc (Exception): Exceção genérica lançada

    Returns:
        JSONResponse: Resposta JSON padronizada contendo:
                      - detail: Mensagem de erro interno do servidor com detalhes da exceção
                      - code: Código de status HTTP (500)
                      - path: Caminho da requisição que gerou o erro

    Note:
        Este handler captura erros inesperados e não deve expor informações
        sensíveis em produção. A mensagem de erro deve ser genérica.
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail=f"Erro interno do servidor: {str(exc)}",
            code="500",
            path=str(request.url),
        ).model_dump(),
    )