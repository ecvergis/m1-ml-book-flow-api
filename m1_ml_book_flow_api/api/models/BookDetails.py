from pydantic import BaseModel

class BookDetails(BaseModel):
    id: int
    title: str
    author: str
    year: int
    score: float
    price_without_tax: float
    price_with_tax: float
    tax: float
    product_type: str
    upc: str
    available: bool
    number_reviews: int

