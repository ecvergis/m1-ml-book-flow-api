from typing import Optional, List, Dict, Union
from ..repositories.top_rating_repository import get_top_rating

def get_ratings(numberItems: int) -> Optional[List[Dict[str, Union[str, float]]]]:
    return get_top_rating(numberItems)
