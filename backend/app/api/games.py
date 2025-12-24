from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies import get_db
from app.models import Game
from app.schemas.game import GameOut

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=List[GameOut])
def list_games(
    year: Optional[int] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
):
    q = db.query(Game)

    if year:
        q = q.filter(Game.date.between(year * 10000, year * 10000 + 1231))

    return q.order_by(Game.date.desc()).limit(limit).all()


@router.get("/{gid}", response_model=GameOut)
def get_game(
    gid: str,
    db: Session = Depends(get_db),
):
    return db.query(Game).filter(Game.gid == gid).one()
