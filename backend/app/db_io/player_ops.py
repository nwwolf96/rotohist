from sqlalchemy.orm import Session
from app.models import Player
from app.common.enums import Handedness

def upsert_player(
    db: Session,
    pid: str,
    first: str = "Unknown",
    last: str = "Unknown",
    bHand: Handedness = Handedness.RIGHT,
    tHand: Handedness = Handedness.RIGHT,
) -> Player:
    player = db.query(Player).filter(Player.pid == pid).first()

    if not player:
        player = Player(
            pid=pid,
            first=first,
            last=last,
            bHand=bHand,
            tHand=tHand,
        )
        db.add(player)
        db.commit()
        db.refresh(player)

    return player
