from fastapi import FastAPI
from m1_ml_book_flow_api.api.routes import books
from m1_ml_book_flow_api.core.handlers import not_found_exception_handler
from m1_ml_book_flow_api.core.exceptions import NotFoundException

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
app.add_exception_handler(404, not_found_exception_handler)

@app.on_event("startup")
async def startup_event():
    print("Starting api...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down api...")
