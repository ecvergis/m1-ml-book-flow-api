from logging import Logger
from typing import List, Optional
from m1_ml_book_flow_api.core.logger import Logger
from ..models.Book import Book
from ..repositories.books_repository import (
    list_books,
    search_books_by,
    get_book_by_id, BOOK_DETAILS
)
from fastapi import HTTPException, status


def list_all_books() -> List[Book]:
    books = list_books()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado")
    return books

def search_all_books(title: Optional[str] = None, category: Optional[str] = None):
    books = search_books_by(title=title, category=category)
    Logger.debug('BOOKS', books)
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum livro encontrado")
    return books

def get_book_details(book_id: int) -> Book:
    book = get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado")
    return book