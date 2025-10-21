from m1_ml_book_flow_api.api.models.book import Book

# BOOKS_DB = [
#     Book(id=1, title="Livro A", author="Autor A", year=2020, category="Ficção", price=29.9, rating=4.5, available=True, image="url_a"),
#     Book(id=2, title="Livro B", author="Autor B", year=2021, category="Romance", price=35.5, rating=4.0, available=True, image="url_b"),
#     Book(id=3, title="Livro C", author="Autor C", year=2022, category="Suspense", price=40.0, rating=4.8, available=False, image="url_c"),
# ]

BOOKS_DB = []

def list_books():
    return BOOKS_DB