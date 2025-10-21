from fastapi import FastAPI
from .api.routes import books

app = FastAPI(
    title="BookFlow API",
    description="Public API for book query",
    version="0.1.0"
)
prefix_api = "/api/v1"
app.include_router(books.router, prefix=prefix_api, tags=["books"])

@app.on_event("startup")
async def startup_event():
    print("Starting api...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down api...")

@app.get("/")
def root():
    return {"message": "Welcome to BookFlow API"}