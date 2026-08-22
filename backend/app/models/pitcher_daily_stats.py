from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import relationship
from app.base import Base
from app.common.enums import Team

class PitcherDailyStats(Base):
    __tablename__ = "pitcher_daily_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)

    gameId = Column(String, ForeignKey("games.gid"), nullable=False, index=True)
    playerId = Column(String, ForeignKey("players.pid"), nullable=False, index=True)

    team = Column(Enum(Team), nullable=False)
    year = Column(Integer, nullable=False)

    appNum = Column(Integer, default=0)
    outs = Column(Integer, default=0)
    noOuts = Column(Integer, default=0)
    bf = Column(Integer, default=0)

    ha = Column(Integer, default=0)
    doubles = Column(Integer, default=0)
    triples = Column(Integer, default=0)
    hr = Column(Integer, default=0)

    r = Column(Integer, default=0)
    er = Column(Integer, default=0)

    bb = Column(Integer, default=0)
    iw = Column(Integer, default=0)
    k = Column(Integer, default=0)
    hbp = Column(Integer, default=0)

    wp = Column(Integer, default=0)
    bk = Column(Integer, default=0)
    sh = Column(Integer, default=0)
    sf = Column(Integer, default=0)

    sb = Column(Integer, default=0)
    cs = Column(Integer, default=0)
    pb = Column(Integer, default=0)

    win_p = Column(Integer, default=0)
    lose_p = Column(Integer, default=0)
    sv = Column(Integer, default=0)

    gs = Column(Integer, default=0)
    gf = Column(Integer, default=0)
    cg = Column(Integer, default=0)
    qs = Column(Integer, default=0)

    visHome = Column(String, nullable=False)

    # relationships
    game = relationship("Game", back_populates="pitcher_daily_stats")
    player = relationship("Player", back_populates="pitcher_daily_stats")

    __table_args__ = (
        Index("ix_pitcher_game_player", "gameId", "playerId"),
    )
