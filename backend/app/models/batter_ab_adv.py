from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.base import Base
from app.common.constants import Team

class PlayerAbAdv(Base):
    __tablename__ = "player_ab_adv"

    id = Column(Integer, primary_key=True)

    batterId = Column(String, ForeignKey("players.pid"), nullable=False)
    pitcherId = Column(String, ForeignKey("players.pid"), nullable=False)
    gameId = Column(String, ForeignKey("games.gid"), nullable=False)

    event = Column(String)
    year = Column(Integer)
    team = Column(Enum(Team))
    bOrder = Column(Integer)

    pa = Column(Integer)
    ab = Column(Integer)
    r = Column(Integer)
    b1 = Column(Integer)
    b2 = Column(Integer)
    b3 = Column(Integer)
    hr = Column(Integer)
    rbi = Column(Integer)
    bb = Column(Integer)
    nump = Column(Integer)
    hbp = Column(Integer)
    sf = Column(Integer)

    sb2 = Column(Integer)
    sb3 = Column(Integer)
    sbh = Column(Integer)
    cs2 = Column(Integer)
    cs3 = Column(Integer)
    csh = Column(Integer)

    sh = Column(Integer)
    iw = Column(Integer)
    xi = Column(Integer)
    bip = Column(Integer)

    ground = Column(Integer)
    fly = Column(Integer)
    line = Column(Integer)
    gdp = Column(Integer)
    othdp = Column(Integer)
    tp = Column(Integer)

    bat_f = Column(String)
    bunt = Column(Integer)
    count = Column(String)
    k = Column(Integer)
    k_safe = Column(Integer)
    wp = Column(Integer)

    outs_pre = Column(Integer)
    outs_post = Column(Integer)

    br1PreId = Column(String, ForeignKey("players.pid"))
    br2PreId = Column(String, ForeignKey("players.pid"))
    br3PreId = Column(String, ForeignKey("players.pid"))
    br1PostId = Column(String, ForeignKey("players.pid"))
    br2PostId = Column(String, ForeignKey("players.pid"))
    br3PostId = Column(String, ForeignKey("players.pid"))

    runHId = Column(String, ForeignKey("players.pid"))
    run1Id = Column(String, ForeignKey("players.pid"))
    run2Id = Column(String, ForeignKey("players.pid"))
    run3Id = Column(String, ForeignKey("players.pid"))

    batter = relationship("Player", foreign_keys=[batterId])
    pitcher = relationship("Player", foreign_keys=[pitcherId])
    game = relationship("Game")

