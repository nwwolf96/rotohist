import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import BatterYearlyStats
from tabulate import tabulate

def query_bs_db(db: Session, year: str):
  # Query BatterYearlyStats for this player
  players = db.query(BatterYearlyStats).filter(BatterYearlyStats.year == year)

  batting_header_season = [
    "Name",
    "Team",
    "GP",
    "BO",
    "L/R",
    "PA",
    "AB",
    "H",
    "R",
    "HR",
    "RBI",
    "BB",
    "SB",
    "CS",
    "AVG",
    "POS",
    "R-Z",
    "HR-Z",
    "RBI-Z",
    "SB-Z",
    "AVG-Z",
    "SUM-Z",
  ]
  rows = [batting_header_season]
  for player in players:
    row = [
      player.playerId,
      player.year,
      player.team,
      player.hand,
      player.gp,
      player.bOrder,
      player.pa,
      player.ab,
      player.h,
      player.r,
      player.hr,
      player.rbi,
      player.bb,
      player.sb,
      player.cs,
      player.pos,
      player.rZ,
      player.hrZ,
      player.rbiZ,
      player.sbZ,
      player.avgZ,
      player.sumZ
    ]
    rows += [row]
  
  print(tabulate(rows, headers="firstrow", tablefmt="fancy_grid"))

if __name__ == "__main__":
  args = sys.argv[1:]
  if "-y" not in args:
    print("Usage: *.py -y year")
    sys.exit(1)

  name_index = args.index("-y") + 1
  name_arg = args[name_index]

  db = SessionLocal()
  try:
    query_bs_db(db, name_arg)
  finally:
    db.close()
