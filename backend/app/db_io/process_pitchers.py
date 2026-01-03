import csv
from sqlalchemy.orm import Session
from app.models import PitcherDailyStats
from app.db_io.player_ops import upsert_player
from app.common.utils import parse_int_or_zero
from app.common.constants import Team

def process_pitchers(db: Session, file_path: str):
  starters: dict[str, dict[str, str]] = {}
  curr_game = ""

  with open(file_path, newline="") as f:
    reader = csv.DictReader(f)

    for raw in reader:
      try:
        if "ALS" in raw["gid"]:
          continue

        if "NLS" in raw["gid"]:
          continue

        if raw["team"] in {"NLS", "ALS"}:
          continue

        gid = raw["gid"]
        pid = raw["id"]

        year = int(gid[3:7])

        if gid != curr_game:
          curr_game = gid
          starters.setdefault(gid, {"spHome": "", "spAway": ""})

        if raw["p_gs"]:
          if raw["vishome"] == "v":
            starters[gid]["spAway"] = pid
          elif raw["vishome"] == "h":
            starters[gid]["spHome"] = pid

        # upsert_player(db, pid)

        stats = PitcherDailyStats(
          gameId=gid,
          playerId=pid,
          team=Team[raw["team"].strip().upper()],
          year=year,
          appNum=parse_int_or_zero(raw["p_seq"]),
          outs=parse_int_or_zero(raw["p_ipouts"]),
          noOuts=parse_int_or_zero(raw["p_noout"]),
          bf=parse_int_or_zero(raw["p_bfp"]),
          ha=parse_int_or_zero(raw["p_h"]),
          doubles=parse_int_or_zero(raw["p_d"]),
          triples=parse_int_or_zero(raw["p_t"]),
          hr=parse_int_or_zero(raw["p_hr"]),
          r=parse_int_or_zero(raw["p_r"]),
          er=parse_int_or_zero(raw["p_er"]),
          bb=parse_int_or_zero(raw["p_w"]),
          iw=parse_int_or_zero(raw["p_iw"]),
          k=parse_int_or_zero(raw["p_k"]),
          hbp=parse_int_or_zero(raw["p_hbp"]),
          wp=parse_int_or_zero(raw["p_wp"]),
          bk=parse_int_or_zero(raw["p_bk"]),
          sh=parse_int_or_zero(raw["p_sh"]),
          sf=parse_int_or_zero(raw["p_sf"]),
          sb=parse_int_or_zero(raw["p_sb"]),
          cs=parse_int_or_zero(raw["p_cs"]),
          pb=parse_int_or_zero(raw["p_pb"]),
          win_p=int(raw["wp"] == "1"),
          lose_p=int(raw["lp"] == "1"),
          sv=int(raw["save"] == "1"),
          gs=int(raw["p_gs"] == "1"),
          gf=parse_int_or_zero(raw["p_gf"]),
          cg=parse_int_or_zero(raw["p_cg"]),
          visHome=raw["vishome"],
        )

        db.add(stats)
        db.commit()

      except Exception as e:
        print("Error processing row: Pitching", raw, e)
        quit()

  return starters
