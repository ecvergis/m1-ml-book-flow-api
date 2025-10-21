from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..services.books_service import get_all_books
from m1_ml_book_flow_api.api.models.book import Book

router = APIRouter()

# GET /api/v1/books
@router.get("/books", response_model=List[Book])
async def list_books():
    return get_all_books()