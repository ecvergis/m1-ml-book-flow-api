from typing import Dict, Union

from pydantic import BaseModel

class StatsOverview(BaseModel):
    total_books: int
    middle_price: float
    distribution_ratings: Dict[Union[int, float], int]