from typing import List

from fastapi import HTTPException, status

from ..models.TopRatedBook import TopRatedBook
from ..repositories.top_rating_repository import get_top_rating
from ...core.logger import Logger


def get_ratings(limit: int) -> List[TopRatedBook]:
    ratings = get_top_rating(limit)
    Logger.debug("Top ratings: %s", ratings)
    if ratings is None:
        ratings = []
    if not ratings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum dado encontrado")
    return ratings
