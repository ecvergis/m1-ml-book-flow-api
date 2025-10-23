from typing import Optional, List
from m1_ml_book_flow_api.api.models.StatsCategories import StatsCategories  # supondo que exista esse model
from m1_ml_book_flow_api.api.services.books_service import list_books

def get_stats_categories() -> Optional[List[StatsCategories]]:
    books = list_books()
    if not books:
        return None

    category_data = {}

    for book in books:
        category = book.category
        if category not in category_data:
            category_data[category] = {"total_price": 0, "count": 0}
        category_data[category]["total_price"] += book.price
        category_data[category]["count"] += 1

    stats = []
    for category, data in category_data.items():
        avg_price = data["total_price"] / data["count"]
        stats.append(
            StatsCategories(
                category_name=category,
                quantity_books=data["count"],
                category_price=round(avg_price, 2)
            )
        )

    return stats
