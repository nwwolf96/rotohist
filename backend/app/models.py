from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import declarative_base
from app.base import Base
from app.common.enums import Handedness

class Player(Base):
    __tablename__ = "players"

    pid = Column(String, primary_key=True, index=True)
    first = Column(String, nullable=False)
    last = Column(String, nullable=False)
    bHand = Column(Enum(Handedness), nullable=False)
    tHand = Column(Enum(Handedness), nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

