from sqlalchemy.orm import Session
from app.models import Game

def process_games_sp(db: Session, starters: dict):
  for gid, sps in starters.items():
    game = db.query(Game).filter(Game.gid == gid).first()
    if not game:
      print(f"Game not found, skipping starter update: {gid}")
      continue

    game.homeSp = sps["spHome"] or None
    game.visSp = sps["spAway"] or None
    db.commit()
