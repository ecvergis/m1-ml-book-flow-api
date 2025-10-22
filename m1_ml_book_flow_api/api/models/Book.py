from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    category: str
    price: float
    rating: float
    available: bool
    image: str