from sqlalchemy import Column, String, Integer, Enum
from sqlalchemy.orm import relationship
from app.base import Base
from app.common.enums import Team

class Game(Base):
    __tablename__ = "games"

    gid = Column(String, primary_key=True, index=True)

    visTeam = Column(Enum(Team), nullable=False)
    homeTeam = Column(Enum(Team), nullable=False)

    date = Column(Integer, nullable=False)
    parkId = Column(String, nullable=False)

    wP = Column(String, nullable=True)
    lP = Column(String, nullable=True)
    svP = Column(String, nullable=True)

    homeSp = Column(String, nullable=True)
    visSp = Column(String, nullable=True)

    # relationships
    pitcher_stats = relationship(
        "PitcherDailyStats",
        back_populates="game",
        cascade="all, delete-orphan",
    )
