# app/db_io/import_fielding.py

import csv
import sys
from sqlalchemy.orm import Session
from app.models import BatterDailyStats

from app.database import SessionLocal

def pos_lookup(pos: int):
  if pos == 1:
    return "PP, "
  elif pos == 2:
    return "CC, "
  elif pos == 3:
    return "1B, "
  elif pos == 4:
    return "2B, "
  elif pos == 5:
    return "3B, "
  elif pos == 6:
    return "SS, "
  elif pos == 7:
    return "LF, "
  elif pos == 8:
    return "CF, "
  elif pos == 9:
    return "RF, "



def process_csv(file_path: str, db: Session):
  """Process CSV and add/update players via FastAPI CRUD."""
  with open(file_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      try:
        gid = row["gid"]
        pid = row["id"]
        team = row["team"]
        gs = int(row["d_gs"])
        seq = int(row["d_seq"])
        dpos = int(row["d_pos"])


        if dpos == 1:
          continue

        if team in ("NLS", "ALS"):
          continue
        record = (
          db.query(BatterDailyStats)
          .filter(
            BatterDailyStats.playerId == pid,
            BatterDailyStats.gameId == gid,
          )
          .first()
        )

        if record:
          record.pos = (record.pos or "") + pos_lookup(dpos)
          if seq == 1:
            record.gs = gs
        else:
          stats = {
            "year": int(gid[3:7]),
            "team": team,
            "bOrder": 0,
            "gp": 1, "gs": 0, "gpdh": 0, "r": 0,
            "lpa": 0, "lab": 0, "lb1": 0, "lb2": 0, "lb3": 0,
            "lhr": 0, "lrbi": 0, "lbb": 0, "lso": 0, "lnump": 0,
            "lhbp": 0, "lsf": 0, "rpa": 0, "rab": 0, "rb1": 0, "rb2": 0,"rb3": 0, "rhr": 0, "rrbi": 0, "rbb": 0, "rso": 0, 
            "rnump": 0, "rhbp": 0, "rsf": 0, "sb": 0, "cs": 0, "pos": "",
          }
          record = BatterDailyStats(
            playerId=pid,
            gameId=gid,
            **stats,
          )
          db.add(record)
          print("Adding event that wasn't recorded")

        db.commit()
        print(f"Processing player: {gid} - {pid}")


      except Exception as e:
        print(f"Error processing row {row.get('id')}: {e}")
        db.rollback()  # reset transaction so we can continue
        quit(1)

  db.close()
  print("CSV processing complete!")


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Usage: python -m app.db_io.import_fielding <path-to-csv>")
    sys.exit(1)

  file_path = sys.argv[1]
  db: Session = SessionLocal()
  process_csv(file_path, db)

