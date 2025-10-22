from ..repositories.books_repository import list_books, search_books, get_book

def get_all_books():
    return list_books()

def search_books(title: str = None, category: str = None):
    return search_books(title, category)

def get_details_book(book_id):
    return get_book(book_id)