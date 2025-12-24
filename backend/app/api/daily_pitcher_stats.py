from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.models import PitcherDailyStats
from app.schemas.pitcher_daily_stats import PitcherDailyStatsOut

router = APIRouter(
    prefix="/pitcher-daily-stats",
    tags=["pitcher-stats"],
)


@router.get("/", response_model=List[PitcherDailyStatsOut])
def list_pitcher_stats(
    game_id: Optional[str] = None,
    player_id: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(PitcherDailyStats)

    if game_id:
        q = q.filter(PitcherDailyStats.gameId == game_id)
    if player_id:
        q = q.filter(PitcherDailyStats.playerId == player_id)
    if year:
        q = q.filter(PitcherDailyStats.year == year)

    return q.limit(limit).all()
