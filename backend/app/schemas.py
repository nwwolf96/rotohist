from pydantic import BaseModel
from app.common.enums import Handedness

class PlayerCreate(BaseModel):
    pid: str
    first: str
    last: str
    bHand: Handedness
    tHand: Handedness

class PlayerOut(PlayerCreate):
    class Config:
        from_attributes = True
