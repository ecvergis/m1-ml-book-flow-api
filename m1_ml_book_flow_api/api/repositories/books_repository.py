from m1_ml_book_flow_api.api.models.Book import Book
from m1_ml_book_flow_api.api.models.BookDetails import BookDetails

# BOOKS_DB = [
#     Book(id=1, title="Livro A", author="Autor A", year=2020, category="Ficção", price=29.9, rating=4.5, available=True, image="url_a"),
#     Book(id=2, title="Livro B", author="Autor B", year=2021, category="Romance", price=35.5, rating=4.0, available=True, image="url_b"),
#     Book(id=3, title="Livro C", author="Autor C", year=2022, category="Suspense", price=40.0, rating=4.8, available=False, image="url_c"),
# ]

BOOKS_DB = []

BOOK_DETAILS = {
    "id": 1,
    "title": "Livro A",
    "author": "Autor A",
    "year": 2025,
    "score": 3.5,
    "price_without_tax": 37.90,
    "price_with_tax": 39.90,
    "tax": 2.00,
    "product_type": "Livro",
    "upc": "hgrf232",
    "available": True,
    "number_reviews": 67
}

def list_books():
    return BOOKS_DB

def get_book(book_id):
    if book_id == BOOK_DETAILS["id"]:
        return BOOK_DETAILS
    else:
        return None

