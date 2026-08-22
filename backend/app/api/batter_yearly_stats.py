from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.batter_yearly_stats import BatterYearlyStatsOut
from app.db_io.batter_yearly_stats_ops import get_batter_yearly_stats

router = APIRouter(prefix="/batter-yearly-stats", tags=["BatterYearlyStats"])

@router.get("/", response_model=list[BatterYearlyStatsOut])
def list_batter_yearly_stats(
    playerId: str | None = None,
    year: int | None = None,
    db: Session = Depends(get_db),
):
    return get_batter_yearly_stats(db, playerId, year)
