from pydantic import BaseModel
from app.common.constants import Team

class BatterDailyStatsOut(BaseModel):
    playerId: str
    gameId: str
    year: int
    team: Team

    bOrder: int | None
    gp: int | None
    lpa: int | None
    lab: int | None
    lr: int | None
    lb1: int | None
    lb2: int | None
    lb3: int | None
    lhr: int | None
    lrbi: int | None
    lbb: int | None
    lso: int | None
    lnump: int | None

    rpa: int | None
    rab: int | None
    rr: int | None
    rb1: int | None
    rb2: int | None
    rb3: int | None
    rhr: int | None
    rrbi: int | None
    rbb: int | None
    rso: int | None
    rnump: int | None
    sb: int | None
    cs: int | None

    class Config:
        from_attributes = True
