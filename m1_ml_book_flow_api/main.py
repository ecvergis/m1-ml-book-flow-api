from fastapi import FastAPI
from m1_ml_book_flow_api.api.routes import books, auth, health, stats_overview, categories, stats_categories
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from m1_ml_book_flow_api.core.handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from fastapi.security import HTTPBearer

security = HTTPBearer()

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
app.include_router(categories.router, prefix=prefix_api, tags=["categories"])
app.include_router(auth.router, prefix=prefix_api, tags=["auth"])
app.include_router(health.router, prefix=prefix_api, tags=["health"])
app.include_router(stats_overview.router, prefix=prefix_api, tags=["stats_overview"])
app.include_router(stats_categories.router, prefix=prefix_api, tags=["stats_categories"])

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

@app.on_event("startup")
async def startup_event():
    print("Starting api...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down api...")
