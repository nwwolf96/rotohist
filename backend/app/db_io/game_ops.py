from sqlalchemy.orm import Session
from app.models import Game
from app.common.constants import Team

def upsert_game(
    db: Session,
    *,
    gid: str,
    vis_team: Team,
    home_team: Team,
    date: int,
    park_id: str,
    wp: str | None,
    lp: str | None,
    svp: str | None,
):
    game = db.query(Game).filter(Game.gid == gid).first()

    if game:
        # Update existing
        game.visTeam = vis_team
        game.homeTeam = home_team
        game.date = date
        game.parkId = park_id
        game.wP = wp
        game.lP = lp
        game.svP = svp
    else:
        # Insert new
        game = Game(
            gid=gid,
            visTeam=vis_team,
            homeTeam=home_team,
            date=date,
            parkId=park_id,
            wP=wp,
            lP=lp,
            svP=svp,
        )
        db.add(game)

    return game
