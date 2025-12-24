import sys
from app.database import SessionLocal
from app.db_io.process_games import process_games_min
from app.db_io.process_pitchers import process_pitchers
from app.db_io.process_games_sp import process_games_sp

def main():
    pitchers = sys.argv[1]
    games = sys.argv[2]

    db = SessionLocal()
    try:
        process_games_min(db, games)
        starters = process_pitchers(db, pitchers)
        process_games_sp(db, starters)
    finally:
        db.close()

if __name__ == "__main__":
    main()
