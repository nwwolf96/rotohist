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
    team: str = "Unknown",
) -> Player:
    player = db.query(Player).filter(Player.pid == pid).first()

    if not player:
        player = Player(
            pid=pid,
            first=first,
            last=last,
            bHand=bHand,
            tHand=tHand,
            team=team,
        )
        db.add(player)
    else:
        # Update existing player
        player.first = first
        player.last = last
        player.bHand = bHand
        player.tHand = tHand
        player.team = player.team + team

    db.commit()
    db.refresh(player)


    return player
