from pydantic import BaseModel
from typing import Optional
from app.common.constants import Team

class PitcherDailyStatsOut(BaseModel):
    gameId: str
    playerId: str
    team: Team
    year: int
    appNum: int
    outs: int
    noOuts: int
    bf: int

    singles: int
    doubles: int
    triples: int
    hr: int
    r: int
    er: int
    bb: int
    k: int

    win_p: int
    lose_p: int
    sv: int
    gs: int
    gf: int
    cg: int

    visHome: str

    class Config:
        from_attributes = True
