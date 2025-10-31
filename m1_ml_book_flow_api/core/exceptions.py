"""
Módulo de exceções personalizadas da API.

Este módulo define exceções customizadas que estendem HTTPException do FastAPI,
fornecendo exceções específicas para diferentes tipos de erros HTTP comuns.
"""
from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    """
    Exceção para recursos não encontrados (404).

    Esta exceção deve ser lançada quando um recurso solicitado não é encontrado
    no sistema.

    Args:
        detail (str): Mensagem de erro descritiva. Padrão: "Recurso não encontrado"
    """
    def __init__(self, detail: str = "Recurso não encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    """
    Exceção para requisições inválidas (400).

    Esta exceção deve ser lançada quando a requisição do cliente contém
    dados inválidos ou malformados.

    Args:
        detail (str): Mensagem de erro descritiva. Padrão: "Requisição inválida"
    """
    def __init__(self, detail: str = "Requisição inválida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    """
    Exceção para requisições não autorizadas (401).

    Esta exceção deve ser lançada quando o cliente não tem permissão para
    acessar o recurso solicitado (credenciais inválidas ou ausentes).

    Args:
        detail (str): Mensagem de erro descritiva. Padrão: "Não autorizado"
    """
    def __init__(self, detail: str = "Não autorizado"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
