from typing import Optional, List, Dict, Union, Any
from ..models.TopRatedBook import TopRatedBook
from ..services.books_service import list_books

def get_top_rating(number_items: int) -> List[TopRatedBook]:
    books = list_books()
    if not books:
        return []

    sorted_books = sorted(books, key=lambda b: b.rating, reverse=True)

    return [TopRatedBook(title=b.title, rating=b.rating) for b in sorted_books[:number_items]]
