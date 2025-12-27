import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Player, BatterDailyStats

def query_bs_db(db: Session, name: str, startDate: str = "", endDate: str = ""):
    # Split name into first and last
    parts = name.split("_")
    if len(parts) != 2:
        print("Name must be in format First_Last")
        sys.exit(1)
    first, last = parts

    # Find the player
    player = db.query(Player).filter(Player.first == first, Player.last == last).first()
    if not player:
        print(f"No player found with name {first} {last}")
        sys.exit(1)

    # Query BatterDailyStats for this player
    stats_query = db.query(BatterDailyStats).filter(BatterDailyStats.playerId == player.pid)

    # Apply date filtering if provided
    if startDate or endDate:
        filtered_records = []
        for record in stats_query:
            # Game ID format: AAAYYYYMMDDX
            gid = record.gameId
            year = gid[3:7]
            month = int(gid[7:9])
            day = int(gid[9:11])
            include = True

            if startDate:
                s_month = int(startDate[4:6])
                s_day = int(startDate[6:8])
                if (month < s_month) or (month == s_month and day < s_day):
                    include = False
            if endDate:
                e_month = int(endDate[4:6])
                e_day = int(endDate[6:8])
                if (month > e_month) or (month == e_month and day > e_day):
                    include = False

            if include:
                filtered_records.append(record)
        stats = filtered_records
    else:
        stats = stats_query.all()

    # Aggregate totals
    total_pa = total_ab = total_hr = total_h = total_b1 = total_b2 = total_b3 = total_rbi = total_r = total_hbp = total_sf = 0
    total_bb = total_so = total_nump = 0
    total_sb = total_cs = 0

    for s in stats:
        print("stat date is " + s.gameId + "r: " + str(s.r) + " " + str(s.lhr + s.rhr))
        total_pa += (s.lpa or 0) + (s.rpa or 0)
        total_ab += (s.lab or 0) + (s.rab or 0)
        total_hr += (s.lhr or 0) + (s.rhr or 0)
        total_b1 += (s.lb1 or 0) + (s.rb1 or 0)
        total_b2 += (s.lb2 or 0) + (s.rb2 or 0)
        total_b3 += (s.lb3 or 0) + (s.rb3 or 0)
        total_hbp += (s.lhbp or 0) + (s.rhbp or 0)
        total_sf += (s.lsf or 0) + (s.rsf or 0)
        total_r += (s.r or 0)
        total_rbi += (s.lrbi or 0) + (s.rrbi or 0)
        total_h += (
            (s.lb1 or 0) + (s.lb2 or 0) + (s.lb3 or 0) + (s.lhr or 0) +
            (s.rb1 or 0) + (s.rb2 or 0) + (s.rb3 or 0) + (s.rhr or 0)
        )
        total_bb += (s.lbb or 0) + (s.rbb or 0)
        total_so += (s.lso or 0) + (s.rso or 0)
        total_nump += (s.lnump or 0) + (s.rnump or 0)
        total_sb += (s.sb or 0)
        total_cs += (s.cs or 0)

    # Calculate derived stats
    avg = total_h / total_ab if total_ab else 0
    obp = (total_h + total_bb + total_hbp) / (total_ab + total_bb + total_hbp + total_sf) if (total_ab + total_bb + total_sf + total_hbp) else 0
    slg = (4*total_hr + 3*total_b3 + 2*total_b2 + total_b1) / total_ab if total_ab else 0  # simplified SLG
    ops = obp + slg

    # Print summary
    print(f"Player: {first} {last}")
    print(f"Games: {len(stats)}")
    print(f"PA: {total_pa}, AB: {total_ab}, H: {total_h}, R: {total_r}, HR: {total_hr}, RBI: {total_rbi}, BB: {total_bb}, SO: {total_so}")
    print(f"SB: {total_sb}, CS: {total_cs}")
    print(f"AVG: {avg:.3f}, OBP: {obp:.3f}, SLG: {slg:.3f}, OPS: {ops:.3f}")
    print(f"NP/AB ratio: {(total_nump / total_ab if total_ab else 0):.3f}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "-n" not in args:
        print("Usage: python get_batter_stats.py -n First_Last [-d YYYYMMDD YYYYMMDD]")
        sys.exit(1)

    name_index = args.index("-n") + 1
    name_arg = args[name_index]

    startDate = endDate = None
    if "-d" in args:
        d_index = args.index("-d") + 1
        startDate = args[d_index]
        endDate = args[d_index + 1]

    db = SessionLocal()
    try:
        query_bs_db(db, name_arg, startDate, endDate)
    finally:
        db.close()
