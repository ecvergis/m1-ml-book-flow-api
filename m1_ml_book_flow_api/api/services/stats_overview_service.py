from typing import Optional
from ..repositories.stats_overview_repository import get_stats_overview
from ..models.StatsOverview import StatsOverview

def get_stats() ->  Optional[StatsOverview]:
    return get_stats_overview()
