import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Player, PitcherDailyStats

def calc_era_whip(ip, ip_chunks, er, bb, ha):
    whole_ip = ip + .333333 * ip_chunks
    ip = whole_ip
    era = ""
    whip = ""
    if float(whole_ip) == 0.0 and float(er) > 0.0:
        era = "INF"
    elif float(er) == 0.0:
        era = "0.00"
    else:
        era = round(float(er)/float(whole_ip)*9.0,4)
        era  = f'{era:.3f}'
    if float(whole_ip) == 0.0 and (float(bb)+float(ha)) > 0:
        whip = "INF"
    elif (float()+float(ha)) == 0.0:
        whip = "0.00"
    else:
        whip = round((float(bb)+float(ha))/(whole_ip),4)
        whip = f'{whip:.3f}'
    return str(era), str(whip)
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

    # Query PitcherDailyStats for this player
    stats_query = db.query(PitcherDailyStats).filter(PitcherDailyStats.playerId == player.pid)

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
    total_gp = total_gs = total_ip = total_er = total_bb = total_ha = total_sb = total_k = total_sv = total_w = 0 
    ip_chunks = 0

    for s in stats:
      total_gp += 1
      total_w += s.win_p
      total_gs += int(s.gs or 0)
      total_ip += float(s.outs or 0.0)
      total_er += s.er
      total_bb += s.bb
      total_k += s.k
      total_sv += s.sv
      total_ha += s.ha 
      total_sb += int(s.sb or 0)

    total_ip /= 3
    if round(float(total_ip)%1,3) == 0.1:
        total_ip -= .1
        ip_chunks += 1
    elif round(float(total_ip)%1,3) == 0.2:
        total_ip -= .2
        ip_chunks += 2

    total_era, total_whip = calc_era_whip(total_ip, ip_chunks, total_er, total_bb, total_ha)
    whole_ip = round(total_ip + .333333 * ip_chunks,2)
    total_ip = whole_ip
    if (total_ip > 0.0):
        total_sbp = round(total_sb / total_ip,3)
    
    positions = []
    min_qualify = 20
    if total_gs >= min_qualify:
        positions += ["SP"]
    if (total_gp - total_gs) >= min_qualify:
        positions += ["RP"]

    # Print summary
    print(f"Player: {first} {last}")
    print(f"Games: {len(stats)}")
    print(f"ha: {total_ha}, bb: {total_bb}")
    print(f"IP: {total_ip}, SO: {total_k}, W: {total_w}, SV: {total_sv}")
    print(f"ERA: {total_era}, WHIP: {total_whip}")


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
