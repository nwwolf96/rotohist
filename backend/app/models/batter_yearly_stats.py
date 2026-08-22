from sqlalchemy import (
    Column, Integer, Float, String, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.base import Base

class BatterYearlyStats(Base):
    __tablename__ = "_yearly_stats"

    Id = Column(Integer, primary_key=True)
    playerId = Column(String, nullable=False)

    year = Column(Integer, nullable=False)
    team = Column(String, nullable=False)
    hand = Column(String, nullable=False)

    bOrder = Column(Integer)
    gp = Column(Integer)
    r = Column(Integer)
    pa = Column(Integer)
    ab = Column(Integer)
    h = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    so = Column(Integer)

    sb = Column(Integer)
    cs = Column(Integer)
    pos = Column(String)

    rZ = Column(Float)
    hrZ = Column(Float)
    rbiZ = Column(Float)
    avgZ = Column(Float)
    sbZ = Column(Float)
    sumZ = Column(Float)


