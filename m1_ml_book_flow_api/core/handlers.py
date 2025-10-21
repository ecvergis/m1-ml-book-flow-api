from fastapi import Request
from fastapi.responses import JSONResponse
from m1_ml_book_flow_api.core.exceptions import NotFoundException

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": exc.detail, "path": str(request.url)}
    )