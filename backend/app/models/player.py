from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from app.base import Base
from app.common.enums import Handedness

class Player(Base):
    __tablename__ = "players"

    pid = Column(String, primary_key=True, index=True)
    first = Column(String, nullable=False)
    last = Column(String, nullable=False)
    bHand = Column(Enum(Handedness), nullable=False)
    tHand = Column(Enum(Handedness), nullable=False)
    team = Column(String, nullable=False)

    pitcher_daily_stats = relationship(
        "PitcherDailyStats",
        back_populates="player",
        cascade="all, delete-orphan",
    )
    batter_daily_stats = relationship(
        "BatterDailyStats",
        foreign_keys="BatterDailyStats.playerId",
        back_populates="player"
    )
