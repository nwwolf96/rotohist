from sqlalchemy.orm import Session
from app.models import BatterDailyStats

def get_batter_daily_stats(
    db: Session,
    player_id: str | None = None,
    game_id: str | None = None,
):
    q = db.query(BatterDailyStats)

    if player_id:
        q = q.filter(BatterDailyStats.playerId == player_id)
    if game_id:
        q = q.filter(BatterDailyStats.gameId == game_id)

    return q.all()
