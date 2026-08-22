from pydantic import BaseModel
from app.common.constants import Team

class BatterYearlyStatsOut(BaseModel):
    playerId: str
    year: int
    team: str
    hand: str

    bOrder: int | None
    gp: int | None
    pa: int | None
    ab: int | None
    r: int | None
    b1: int | None
    b2: int | None
    b3: int | None
    hr: int | None
    rbi: int | None
    bb: int | None
    so: int | None

    rZ = float | None
    hrZ = float | None
    rbiZ = float | None
    avgZ = float | None
    sbZ = float | None
    sumZ = float | None

    class Config:
        from_attributes = True
