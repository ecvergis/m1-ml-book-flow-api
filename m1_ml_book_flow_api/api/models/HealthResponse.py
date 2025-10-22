from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    total_books: Optional[int] = None
    message: Optional[str] = None