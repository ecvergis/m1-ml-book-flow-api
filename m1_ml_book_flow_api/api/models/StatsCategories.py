from pydantic import BaseModel

class StatsCategories(BaseModel):
    category_name: str
    quantity_books: int
    category_price: float