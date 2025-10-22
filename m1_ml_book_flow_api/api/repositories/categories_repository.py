from m1_ml_book_flow_api.api.repositories.books_repository import list_books

def list_categories():
    categories = set()
    books = list_books()
    for book in books:
        if getattr(book, "category", None):
            categories.add(book.category)
    return sorted(list(categories))