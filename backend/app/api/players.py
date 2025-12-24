from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.models import Player
from app.schemas.player import PlayerCreate, PlayerOut
from app.api.player import create_player

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=PlayerOut)
def upsert_player(
    player: PlayerCreate,
    db: Session = Depends(get_db),
):
    return create_player(
        db=db,
        pid=player.pid,
        first=player.first,
        last=player.last,
        bHand=player.bHand,
        tHand=player.tHand,
    )

@router.get("/", response_model=List[PlayerOut])
def list_players(db: Session = Depends(get_db)):
    return db.query(Player).all()

