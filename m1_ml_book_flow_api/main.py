from fastapi import FastAPI
from m1_ml_book_flow_api.api.routes import books
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from m1_ml_book_flow_api.core.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title="BookFlow API",
    description="""
API pública desenvolvida como projeto da Pós Tech em Machine Learning da FIAP. Fornece dados de livros processados para sistemas de recomendação e análise, integrando etapas de extração, transformação e disponibilização. Projetada com foco em escalabilidade, modularidade e reuso em modelos de aprendizado de máquina.
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
prefix_api = "/api/v1"
app.include_router(books.router, prefix=prefix_api, tags=["books"])
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.on_event("startup")
async def startup_event():
    print("Starting api...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down api...")
