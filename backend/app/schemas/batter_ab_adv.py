from pydantic import BaseModel
from app.common.constants import Team

class PlayerAbAdvOut(BaseModel):
    id: int
    batterId: str
    pitcherId: str
    gameId: str
    event: str | None
    year: int | None
    team: Team | None

    pa: int | None
    ab: int | None
    hr: int | None
    rbi: int | None

    class Config:
        from_attributes = True
