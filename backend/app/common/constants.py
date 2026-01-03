from dataclasses import dataclass
from typing import Optional
from app.common.enums import Team, Position

# ---- Core Data Classes ----

@dataclass
class Starters:
    spHome: str
    spAway: str

@dataclass
class PlayerStats:
    year: int
    team: Team
    bOrder: int
    gp: int
    lpa: int
    lab: int
    lr: int
    lb1: int
    lb2: int
    lb3: int
    lhr: int
    lrbi: int
    lbb: int
    lso: int
    lnump: int
    rpa: int
    rab: int
    rr: int
    rb1: int
    rb2: int
    rb3: int
    rhr: int
    rrbi: int
    rbb: int
    rso: int
    rnump: int
    sb: int
    cs: int

# ---- Raw CSV Rows ----

@dataclass
class RawPaRow:
    gid: str
    event: str
    batter: str
    batteam: str
    pitcher: str
    count: str
    pithand: str
    border: str
    bat_f: str
    pa: str
    ab: str
    single: str
    double: str
    triple: str
    hr: str
    k: str
    xi: str
    nump: str
    hbp: str
    sh: str
    iw: str
    bb: str
    sf: str
    bip: str
    bunt: str
    ground: str
    fly: str
    line: str
    gdp: str
    othdp: str
    tp: str
    wp: str
    sb2: str
    sb3: str
    sbh: str
    cs2: str
    cs3: str
    csh: str
    k_s: str
    r: str
    rbi: str
    outs_pre: str
    outs_post: str
    br1_pre: Optional[str] = None
    br2_pre: Optional[str] = None
    br3_pre: Optional[str] = None
    br1_post: Optional[str] = None
    br2_post: Optional[str] = None
    br3_post: Optional[str] = None
    run_b: Optional[str] = None
    run1: Optional[str] = None
    run2: Optional[str] = None
    run3: Optional[str] = None

@dataclass
class RawGameRow:
    gid: str
    visteam: str
    hometeam: str
    date: str
    parkId: str
    wP: Optional[str] = None
    lP: Optional[str] = None
    svP: Optional[str] = None

@dataclass
class RawPitcherRow:
    gid: str
    id: str
    team: str
    p_seq: str
    p_ipouts: str
    p_noouts: str
    p_bfp: str
    p_h: str
    p_d: str
    p_t: str
    p_hr: str
    p_r: str
    p_er: str
    p_w: str
    p_iw: str
    p_k: str
    p_hbp: str
    p_wp: str
    p_bk: str
    p_sh: str
    p_sf: str
    p_sb: str
    p_cs: str
    p_pb: str
    wp: Optional[str] = None
    lp: Optional[str] = None
    save: Optional[str] = None
    p_gs: Optional[str] = None
    p_gf: Optional[str] = None
    p_cg: Optional[str] = None
    p_vh: Optional[str] = None

@dataclass
class RawPlayerRow:
    pid: str
    first: str
    last: str
    bHand: str
    tHand: str
    team: str

