from sqlalchemy import (
    Column, Integer, String, Enum, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.base import Base
from app.common.constants import Team

class BatterDailyStats(Base):
    __tablename__ = "_daily_stats"

    Id = Column(Integer, primary_key=True)
    playerId = Column(String, ForeignKey("players.pid"), nullable=False)
    gameId = Column(String, ForeignKey("games.gid"), nullable=False)

    year = Column(Integer, nullable=False)
    team = Column(Enum(Team), nullable=False)

    bOrder = Column(Integer)
    gp = Column(Integer)
    lpa = Column(Integer)
    lab = Column(Integer)
    lr = Column(Integer)
    lb1 = Column(Integer)
    lb2 = Column(Integer)
    lb3 = Column(Integer)
    lhr = Column(Integer)
    lrbi = Column(Integer)
    lbb = Column(Integer)
    lso = Column(Integer)
    lnump = Column(Integer)

    rpa = Column(Integer)
    rab = Column(Integer)
    rr = Column(Integer)
    rb1 = Column(Integer)
    rb2 = Column(Integer)
    rb3 = Column(Integer)
    rhr = Column(Integer)
    rrbi = Column(Integer)
    rbb = Column(Integer)
    rso = Column(Integer)
    rnump = Column(Integer)

    sb = Column(Integer)
    cs = Column(Integer)

    game = relationship("Game")

    game = relationship("Game", back_populates="batter_daily_stats")
    player = relationship("Player", back_populates="batter_daily_stats")

    __table_args__ = (
        UniqueConstraint("playerId", "gameId", name="uq_player_game"),
    )

