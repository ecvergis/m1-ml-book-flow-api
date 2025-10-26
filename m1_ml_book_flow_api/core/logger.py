import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime
import os

class CustomJsonFormatter(jsonlogger.JsonFormatter):
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
    return logging.getLogger(f"BookFlow.{name}")

def log_request(method: str, path: str, status_code: int, duration: float, user_id: str = None, **kwargs):
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
