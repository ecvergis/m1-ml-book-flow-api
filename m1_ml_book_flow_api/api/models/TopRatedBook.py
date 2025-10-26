from pydantic import BaseModel

class TopRatedBook(BaseModel):
    title: str
    rating: float
