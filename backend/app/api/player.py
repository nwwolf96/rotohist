from sqlalchemy.orm import Session
from app.models import Player
from app.common.enums import Handedness

def create_player(
    db: Session,
    pid: str,
    first: str,
    last: str,
    bHand: Handedness,
    tHand: Handedness,
    team: str,
) -> Player:
    """
    Insert a new player or update existing player based on pid.
    Mimics Prisma's upsert behavior.
    """
    player = db.query(Player).filter(Player.pid == pid).first()
    if player:
        # Update existing player
        player.first = first
        player.last = last
        player.bHand = bHand
        player.tHand = tHand
        player.team = player.team + team
    else:
        # Create new player
        player = Player(
            pid=pid,
            first=first,
            last=last,
            bHand=bHand,
            tHand=tHand,
            team=team,
        )
        db.add(player)
    
    db.commit()
    db.refresh(player)
    return player

