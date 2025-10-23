from typing import Optional
from ..repositories.stats_categories_repository import get_stats_categories
from ..models.StatsOverview import StatsOverview

def get_stats() ->  Optional[StatsOverview]:
    return get_stats_categories()
