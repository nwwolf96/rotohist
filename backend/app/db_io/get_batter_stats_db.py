from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Player, PlayerAbAdv

def query_bs_db(db: Session, name: str, startDate: str = None, endDate: str = None):
    """
    Query batter events for a player, filtering by date extracted from gameId.
    - name: 'First_Last'
    - startDate, endDate: 'YYYYMMDD' strings
    """
    first_last = name.split("_")
    if len(first_last) != 2:
        print("Name should be in 'First_Last' format")
        return

    first, last = first_last

    player = db.query(Player).filter(
        Player.first.ilike(first),
        Player.last.ilike(last)
    ).first()

    if not player:
        print(f"No player found with name {first} {last}")
        return

    events = db.query(PlayerAbAdv).filter(
        (PlayerAbAdv.batterId == player.pid) |
        (PlayerAbAdv.br1PreId == player.pid) |
        (PlayerAbAdv.br2PreId == player.pid) |
        (PlayerAbAdv.br3PreId == player.pid)
    ).all()

    # Parse date range
    min_mon, min_day = 3, 20
    max_mon, max_day = 9, 30

    if startDate:
        min_mon = int(startDate[4:6])
        min_day = int(startDate[6:8])
    if endDate:
        max_mon = int(endDate[4:6])
        max_day = int(endDate[6:8])

    # Aggregated stats
    hr = r = rbi = h = b1 = b2 = b3 = ab = pa = bb = so = sb2 = sb3 = sbh = cs2 = cs3 = csh = nump = hbp = sf = 0

    for e in events:
        month = int(e.gameId[7:9])
        day = int(e.gameId[9:11])

        if not (min_mon <= month <= max_mon):
            continue
        if month == min_mon and day < min_day:
            continue
        if month == max_mon and day > max_day:
            continue

        if e.batterId == player.pid:
            print("pid and gid are " + player.pid + " " + e.gameId)
            hr += e.hr
            rbi += e.rbi
            h += e.b1 + e.b2 + e.b3 + e.hr
            b1 += e.b1
            b2 += e.b2
            b3 += e.b3
            ab += e.ab
            pa += e.pa
            bb += e.bb
            so += e.k
            nump += e.nump
            hbp += e.hbp
            sf += e.sf

        if player.pid in [e.run1Id, e.run2Id, e.run3Id]:
            r += 1

        if player.pid == e.br1PreId:
            sb2 += e.sb2
            cs2 += e.cs2
        if player.pid == e.br2PreId:
            sb3 += e.sb3
            cs3 += e.cs3
        if player.pid == e.br3PreId:
            sbh += e.sbh
            csh += e.csh

    print(f"{first} {last} Stats:")
    print(f"HR: {hr}, R: {r+hr}, RBI: {rbi}, H: {h}, AB: {ab}, PA: {pa}")
    print(f"SB: {sb2+sb3+sbh} (sb2:{sb2}, sb3:{sb3}, sbh:{sbh})")
    print(f"CS: {cs2+cs3+csh} (cs2:{cs2}, cs3:{cs3}, csh:{csh})")
    avg = h/ab if ab else 0
    obp = (h + bb + hbp) / (ab + bb + hbp + sf) if (ab + bb + hbp + sf) else 0
    slg = (b1 + 2*b2 + 3*b3 + 4*hr) / ab if ab else 0
    ops = obp + slg
    print(f"AVG: {avg:.3f}, OBP: {obp:.3f}, SLG: {slg:.3f}, OPS: {ops:.3f}, Nump/AB: {(nump/ab if ab else 0):.3f}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Query batter events from DB")
    parser.add_argument("-n", "--name", required=True, help="Player name First_Last")
    parser.add_argument("-d", "--dates", nargs=2, help="Start and end date YYYYMMDD YYYYMMDD")
    args = parser.parse_args()

    db = SessionLocal()
    start_date = end_date = None
    if args.dates:
        start_date, end_date = args.dates

    query_bs_db(db, args.name, start_date, end_date)


if __name__ == "__main__":
    main()
