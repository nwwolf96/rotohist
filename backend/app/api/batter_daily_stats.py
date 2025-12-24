from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.batter_daily_stats import BatterDailyStatsOut
from app.db_io.batter_daily_stats_ops import get_batter_daily_stats

router = APIRouter(prefix="/batter-daily-stats", tags=["BatterDailyStats"])

@router.get("/", response_model=list[BatterDailyStatsOut])
def list_batter_daily_stats(
    playerId: str | None = None,
    gameId: str | None = None,
    db: Session = Depends(get_db),
):
    return get_batter_daily_stats(db, playerId, gameId)
