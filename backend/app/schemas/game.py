from pydantic import BaseModel
from typing import Optional
from app.common.constants import Team

class GameOut(BaseModel):
    gid: str
    visTeam: Team
    homeTeam: Team
    date: int
    parkId: str
    wP: Optional[str]
    lP: Optional[str]
    svP: Optional[str]
    homeSp: Optional[str]
    visSp: Optional[str]

    class Config:
        from_attributes = True
