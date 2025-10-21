from ..repositories.books_repository import list_books, get_book

def get_all_books():
    return list_books()

def get_details_book(book_id):
    return get_book(book_id)