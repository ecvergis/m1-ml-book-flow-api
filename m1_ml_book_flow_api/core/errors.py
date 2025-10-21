from pydantic import BaseModel, Field
from typing import Optional

class ErrorResponse(BaseModel):
    detail: str
    code: str
    path: Optional[str] = None