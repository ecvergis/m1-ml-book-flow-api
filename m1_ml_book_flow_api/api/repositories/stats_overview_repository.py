from typing import Optional, Counter
from ..models.StatsOverview import StatsOverview
from ..repositories.books_repository import list_books

def get_stats_overview() -> Optional[StatsOverview]:
    books = list_books()
    if len(books) == 0:
        return None
    else:
        middle_price = sum(book.price for book in books) / len(books)
        ratings = [book.rating for book in books if getattr(book, "rating", None) is not None]
        distribution_ratings = dict(Counter(ratings))

        stats = StatsOverview(
            total_books=len(books),
            middle_price=middle_price,
            distribution_ratings=distribution_ratings
        )
    return stats