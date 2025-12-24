import csv
import sys
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import BatterDailyStats, PlayerAbAdv
from app.common.constants import Team
from app.common.enums import Handedness
from app.db_io.player_ops import upsert_player
from app.common.utils import parse_int_or_zero


def lookup_hand(hand: str, expected: Handedness) -> bool:
  if hand == "L":
    hand = "LEFT"
  elif hand == "R":
    hand = "RIGHT"
  return hand == expected.name


def init_player_stats(stats: dict, player_id: str, year: int, team: Team, b_order: int):
  if player_id not in stats:
    stats[player_id] = {
      "year": year,
      "team": team,
      "bOrder": b_order,
      "gp": 1,
      "lpa": 0, "lab": 0, "lr": 0, "lb1": 0, "lb2": 0, "lb3": 0,
      "lhr": 0, "lrbi": 0, "lbb": 0, "lso": 0, "lnump": 0,
      "rpa": 0, "rab": 0, "rr": 0, "rb1": 0, "rb2": 0, "rb3": 0,
      "rhr": 0, "rrbi": 0, "rbb": 0, "rso": 0, "rnump": 0,
      "sb": 0, "cs": 0,
    }


def flush_daily_stats(db: Session, game_id: str, stats: dict):
  for player_id, s in stats.items():
    record = (
      db.query(BatterDailyStats)
      .filter(
        BatterDailyStats.playerId == player_id,
        BatterDailyStats.gameId == game_id,
      )
      .first()
    )

    if record:
      for k, v in s.items():
        setattr(record, k, v)
    else:
      record = BatterDailyStats(
        playerId=player_id,
        gameId=game_id,
        **s,
      )
      db.add(record)

  db.commit()


def process_pa_csv(db: Session, file_path: str):
  print("processing 2024 plays csv")
  curr_game = ""
  game_stats: dict[str, dict] = {}

  with open(file_path, newline="") as f:
    reader = csv.DictReader(f)

    for raw in reader:
      try:
        if "ALS" in raw["gid"]:
          continue

        gid = raw["gid"]
        batter = raw["batter"]
        pitcher = raw["pitcher"]
        year = int(gid[3:7])
        team = Team[raw["batteam"].strip().upper()]
        b_order = parse_int_or_zero(raw["lp"])

        upsert_player(db, batter)
        upsert_player(db, pitcher)

        if curr_game and gid != curr_game:
          flush_daily_stats(db, curr_game, game_stats)
          game_stats = {}

        curr_game = gid

        init_player_stats(game_stats, batter, year, team, b_order)
        s = game_stats[batter]

        if lookup_hand(raw["pithand"], Handedness.LEFT):
          s["lpa"] += parse_int_or_zero(raw["pa"])
          s["lab"] += parse_int_or_zero(raw["ab"])
          s["lr"] += parse_int_or_zero(raw["runs"])
          s["lb1"] += parse_int_or_zero(raw["single"])
          s["lb2"] += parse_int_or_zero(raw["double"])
          s["lb3"] += parse_int_or_zero(raw["triple"])
          s["lhr"] += parse_int_or_zero(raw["hr"])
          s["lrbi"] += parse_int_or_zero(raw["rbi"])
          s["lbb"] += parse_int_or_zero(raw["walk"])
          s["lso"] += parse_int_or_zero(raw["k_safe"])
          s["lnump"] += parse_int_or_zero(raw["nump"])
        else:
          s["rpa"] += parse_int_or_zero(raw["pa"])
          s["rab"] += parse_int_or_zero(raw["ab"])
          s["rr"] += parse_int_or_zero(raw["runs"])
          s["rb1"] += parse_int_or_zero(raw["single"])
          s["rb2"] += parse_int_or_zero(raw["double"])
          s["rb3"] += parse_int_or_zero(raw["triple"])
          s["rhr"] += parse_int_or_zero(raw["hr"])
          s["rrbi"] += parse_int_or_zero(raw["rbi"])
          s["rbb"] += parse_int_or_zero(raw["walk"])
          s["rso"] += parse_int_or_zero(raw["k_safe"])
          s["rnump"] += parse_int_or_zero(raw["nump"])

        s["sb"] += (
          parse_int_or_zero(raw["sb2"])
          + parse_int_or_zero(raw["sb3"])
          + parse_int_or_zero(raw["sbh"])
        )
        s["cs"] += (
          parse_int_or_zero(raw["cs2"])
          + parse_int_or_zero(raw["cs3"])
          + parse_int_or_zero(raw["csh"])
        )

        ab = PlayerAbAdv(
          batterId=batter,
          pitcherId=pitcher,
          gameId=gid,
          event=raw["event"],
          year=year,
          team=team,
          bOrder=b_order,
          bat_f=raw["bat_f"],
          count=raw["count"],
          pa=parse_int_or_zero(raw["pa"]),
          ab=parse_int_or_zero(raw["ab"]),
          b1=parse_int_or_zero(raw["single"]),
          b2=parse_int_or_zero(raw["double"]),
          b3=parse_int_or_zero(raw["triple"]),
          hr=parse_int_or_zero(raw["hr"]),
          k=parse_int_or_zero(raw["k"]),
          nump=parse_int_or_zero(raw["nump"]),
          hbp=parse_int_or_zero(raw["hbp"]),
          sh=parse_int_or_zero(raw["sh"]),
          sf=parse_int_or_zero(raw["sf"]),
          iw=parse_int_or_zero(raw["iw"]),
          bb=parse_int_or_zero(raw["walk"]),
          xi=parse_int_or_zero(raw["xi"]),
          bip=parse_int_or_zero(raw["bip"]),
          bunt=parse_int_or_zero(raw["bunt"]),
          ground=parse_int_or_zero(raw["ground"]),
          fly=parse_int_or_zero(raw["fly"]),
          line=parse_int_or_zero(raw["line"]),
          gdp=parse_int_or_zero(raw["gdp"]),
          othdp=parse_int_or_zero(raw["othdp"]),
          tp=parse_int_or_zero(raw["tp"]),
          wp=parse_int_or_zero(raw["wp"]),
          sb2=parse_int_or_zero(raw["sb2"]),
          sb3=parse_int_or_zero(raw["sb3"]),
          sbh=parse_int_or_zero(raw["sbh"]),
          cs2=parse_int_or_zero(raw["cs2"]),
          cs3=parse_int_or_zero(raw["cs3"]),
          csh=parse_int_or_zero(raw["csh"]),
          k_safe=parse_int_or_zero(raw["k_safe"]),
          r=parse_int_or_zero(raw["runs"]),
          rbi=parse_int_or_zero(raw["rbi"]),
          outs_pre=parse_int_or_zero(raw["outs_pre"]),
          outs_post=parse_int_or_zero(raw["outs_post"]),
          br1PreId=raw["br1_pre"] or None,
          br2PreId=raw["br2_pre"] or None,
          br3PreId=raw["br3_pre"] or None,
          br1PostId=raw["br1_post"] or None,
          br2PostId=raw["br2_post"] or None,
          br3PostId=raw["br3_post"] or None,
          runHId=raw["run_b"] or None,
          run1Id=raw["run1"] or None,
          run2Id=raw["run2"] or None,
          run3Id=raw["run3"] or None,
        )

        db.add(ab)
        db.commit()

      except Exception as e:
        print("Error processing row:", raw, e)
        quit(1)

  if curr_game and game_stats:
    flush_daily_stats(db, curr_game, game_stats)

  print("CSV processing complete")

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python -m app.db_io.load_pa_stats <path-to-csv>")
        sys.exit(1)

    db = SessionLocal()
    file_path = sys.argv[1]
    process_pa_csv(db, file_path)

