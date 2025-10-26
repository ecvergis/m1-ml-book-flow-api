from typing import Optional, List, Dict, Union
from m1_ml_book_flow_api.api.services.books_service import list_books

def get_top_rating(numberItems: int) -> Optional[List[Dict[str, Union[str, float]]]]:
    books = list_books()
    if not books:
        return None

    sorted_books = sorted(
        books,
        key=lambda b: b.get('rating', 0),
        reverse=True
    )

    top_books = [
        {
            "name": book.get("name"),
            "rating": book.get("rating")
        }
        for book in sorted_books[:numberItems]
    ]

    return top_books
