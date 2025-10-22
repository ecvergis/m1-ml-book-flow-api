from ..repositories.books_repository import list_books

def get_books_count() -> int:
    books = list_books()
    return len(books)