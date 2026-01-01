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
        seq = row["b_seq"]
        if seq == '':
          continue
        else:
          seq = int(seq)
        dh = row["dh"]
        if dh == '':
          continue
        else:
          dh = int(dh)

        record = (
          db.query(BatterDailyStats)
          .filter(
            BatterDailyStats.playerId == pid,
            BatterDailyStats.gameId == gid,
          )
          .first()
        )

        if record:
          record.pos = (record.pos or "") + "DH, "
          if seq == 1 and dh == 1:
            record.gs = 1
        else:
          print("player apparently didn't have an event / steal")

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

