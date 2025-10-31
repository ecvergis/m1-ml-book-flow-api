"""
Módulo de configuração de logging estruturado.

Este módulo configura o sistema de logging da aplicação para usar formato JSON,
facilitando a integração com ferramentas de análise de logs e monitoramento.
Fornece funções utilitárias para logging de requisições HTTP, eventos de autenticação
e erros.
"""
import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime
import os

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formatador JSON personalizado para logs estruturados.

    Estende JsonFormatter para adicionar campos padronizados a todos os logs,
    incluindo timestamp, level, service e version.

    Attributes:
        timestamp: Data e hora UTC do log em formato ISO
        level: Nível do log em maiúsculas
        service: Nome do serviço (book-flow-api)
        version: Versão da aplicação (1.0.0)
    """
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            log_record['timestamp'] = datetime.utcnow().isoformat()
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        log_record['service'] = 'book-flow-api'
        log_record['version'] = '1.0.0'

handler = logging.StreamHandler(sys.stdout)
formatter = CustomJsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s %(pathname)s %(lineno)d %(funcName)s'
)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)

logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

Logger = logging.getLogger("BookFlow")
Logger.setLevel(logging.DEBUG)

def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger nomeado para um módulo específico.

    Cria ou retorna um logger com o nome "BookFlow.{name}", permitindo
    identificação fácil do módulo que gerou o log.

    Args:
        name (str): Nome do módulo ou componente (ex: "books_service", "auth")

    Returns:
        logging.Logger: Logger configurado para o módulo especificado
    """
    return logging.getLogger(f"BookFlow.{name}")

def log_request(method: str, path: str, status_code: int, duration: float, user_id: str = None, **kwargs):
    """
    Registra uma requisição HTTP com informações detalhadas.

    Cria um log estruturado para requisições HTTP, incluindo método, caminho,
    código de status, duração e informações do usuário.

    Args:
        method (str): Método HTTP da requisição (GET, POST, etc.)
        path (str): Caminho da requisição
        status_code (int): Código de status HTTP da resposta
        duration (float): Duração da requisição em segundos
        user_id (str, optional): ID do usuário autenticado (se disponível)
        **kwargs: Campos adicionais para incluir no log (request_id, client_ip, etc.)
    """
    logger = get_logger("http")
    logger.info(
        "HTTP Request",
        extra={
            "http_method": method,
            "http_path": path,
            "http_status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            "user_id": user_id,
            **kwargs
        }
    )

def log_auth_event(event_type: str, user_id: str = None, success: bool = True, **kwargs):
    """
    Registra um evento de autenticação.

    Cria um log estruturado para eventos relacionados à autenticação,
    como login, logout, refresh token, etc.

    Args:
        event_type (str): Tipo do evento (ex: "login_success", "login_failed", "refresh_success")
        user_id (str, optional): ID do usuário relacionado ao evento
        success (bool): Se o evento foi bem-sucedido. Padrão: True
        **kwargs: Campos adicionais para incluir no log (username, reason, etc.)
    """
    logger = get_logger("auth")
    logger.info(
        f"Auth Event: {event_type}",
        extra={
            "auth_event": event_type,
            "user_id": user_id,
            "success": success,
            **kwargs
        }
    )

def log_error(error: Exception, context: str = None, **kwargs):
    """
    Registra um erro com informações detalhadas.

    Cria um log estruturado para erros, incluindo tipo do erro, mensagem,
    contexto e stack trace completo.

    Args:
        error (Exception): Exceção que foi lançada
        context (str, optional): Contexto onde o erro ocorreu (ex: nome da função, módulo)
        **kwargs: Campos adicionais para incluir no log (request_id, http_method, etc.)
    """
    logger = get_logger("error")
    logger.error(
        f"Error: {str(error)}",
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            **kwargs
        },
        exc_info=True
    )
