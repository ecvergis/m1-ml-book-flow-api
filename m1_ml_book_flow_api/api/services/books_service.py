from ..repositories.books_repository import list_books
from m1_ml_book_flow_api.core.exceptions import NotFoundException

def get_all_books():
    return list_books()