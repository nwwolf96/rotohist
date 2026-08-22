from sqlalchemy.orm import Session
from app.models import BatterYearlyStats

def get_batter_yearly_stats(
    db: Session,
    player_id: str | None = None,
    year: int | None = None,
):
    q = db.query(BatterYearlyStats)

    if player_id:
        q = q.filter(BatterYearlyStats.playerId == player_id)
    if year:
        q = q.filter(BatterYearlyStats.year == year)

    return q.all()
