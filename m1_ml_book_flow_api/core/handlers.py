from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from m1_ml_book_flow_api.core.errors import ErrorResponse


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Trata exceções HTTP levantadas manualmente (404, 400, etc.)
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
    Trata erros automáticos de validação do Pydantic / FastAPI
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
    Captura qualquer erro inesperado (não tratado)
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail=f"Erro interno do servidor: {str(exc)}",
            code="500",
            path=str(request.url),
        ).model_dump(),
    )