import csv
from sqlalchemy.orm import Session
from app.models import Game
from app.common.constants import Team
from app.db_io.game_ops import upsert_game

def process_games_min(db: Session, file_path: str):
  with open(file_path, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
      try:
        vis = row["visteam"].strip().upper()
        home = row["hometeam"].strip().upper()
        if vis in {"NLS", "ALS"} or home in {"NLS", "ALS"}:
          continue

        upsert_game(
          db,
          gid=row["gid"],
          vis_team=Team[row["visteam"].strip().upper()],
          home_team=Team[row["hometeam"].strip().upper()],
          date=int(row["date"]),
          park_id=row["site"],
          wp=row["wp"] or None,
          lp=row["lp"] or None,
          svp=row["save"] or None,
        )

        db.commit()

      except Exception as e:
        print("Error processing row: Games:", row, e)
        quit()
