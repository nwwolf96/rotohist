# app/db_io/add_players.py

import csv
import sys
from sqlalchemy.orm import Session
from app.common.constants import RawPlayerRow
from app.common.enums import Handedness
from app.api.player import create_player  

from app.database import SessionLocal


def parse_hand(hand: str) -> Handedness:
    """Convert CSV hand string to Handedness enum."""
    hand = hand.upper()
    if hand == "R":
        return Handedness.RIGHT
    elif hand in ("B", "S"):
        return Handedness.SWITCH
    else:
        return Handedness.LEFT


def process_csv(file_path: str):
    """Process CSV and add/update players via FastAPI CRUD."""
    db: Session = SessionLocal()
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                filtered = RawPlayerRow(
                    pid=row.get("id", ""),
                    last=row.get("last", ""),
                    first=row.get("first", ""),
                    bHand=row.get("bat", ""),
                    tHand=row.get("throw", ""),
                )

                bat_hand = parse_hand(filtered.bHand)
                throw_hand = parse_hand(filtered.tHand)

                print(f"Processing player: {filtered.pid} - {filtered.first} {filtered.last}")

                # Use your FastAPI CRUD function
                create_player(
                    db=db,
                    pid=filtered.pid,
                    first=filtered.first,
                    last=filtered.last,
                    bHand=bat_hand,
                    tHand=throw_hand,
                )

            except Exception as e:
                print(f"Error processing row {row.get('id')}: {e}")
                db.rollback()  # reset transaction so we can continue

    db.close()
    print("CSV processing complete!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.db_io.add_players <path-to-csv>")
        sys.exit(1)

    file_path = sys.argv[1]
    process_csv(file_path)

