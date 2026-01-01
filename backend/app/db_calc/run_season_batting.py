import app.db_calc.season_batting as sb
import app.db_calc.season_commons as sc
from app.database import SessionLocal

TOTAL_DAYS_SEASON = 186
ab_min = 25
min_qualify = 20

total_days = sc.dateToNumber(sc.args.to)-sc.dateToNumber(sc.args.fro)
if total_days > TOTAL_DAYS_SEASON:
    total_days = TOTAL_DAYS_SEASON

min_qualify = min_qualify*(total_days/TOTAL_DAYS_SEASON)
ab_min = ab_min*(total_days/TOTAL_DAYS_SEASON)
# ab_min = ab_min*(total_days)

print("Sample from " + sc.args.fro + " to " + sc.args.to + " | total days: " + str(total_days))

TEAM_SIZE = 12
POS_CT = {"CC": 2, "SS": 1, "2B": 1, "3B": 1, "OF": 5, "1B": 1, "2BorSS": 1, "1Bor3B": 1, "UTIL": 1}
# POS_CT = {"CC": 2, "SS": 2, "2B": 2, "3B": 2, "OF": 6, "1B": 2, "UTIL": 2}
AUCT_POS = "R"
POS_ORDER = ["CC","SS","2B","3B","OF","1B","2BorSS","1Bor3B","UTIL"]
# POS_ORDER = ["CC","SS","2B","3B","OF","1B","UTIL"]
NAMES_FROM_FILE = False

db = SessionLocal()
# TODO fix this... this is a bit of a hack, i need to change the db to store the date value that I calculated in commons
if "10/" in sc.args.to:
    people = sc.get_names_from_file("files/2023_people/hitters_fmt.out")
    all_player_ats = sc.load_all_ats(people, min_qualify, sb.loadBatterStatsFromDb)
else:
    people = sc.load_names_from_year(db, sc.args.fro, sc.args.to, sc.PlayerType.HITTER)
    all_player_ats = sc.load_all_ats(db, people, min_qualify, sb.loadBatterStatsFromDb)

player_list = sb.fill_buckets(all_player_ats, TEAM_SIZE, POS_CT, POS_ORDER)

league_ba = sb.get_league_ba(player_list, all_player_ats, ab_min=0)
total_r, total_hr, total_rbi, total_sb, total_hoa,_,_= sb.sample_players(player_list, all_player_ats, league_ba, eval_prv=False, ab_min=int(ab_min), print_players=False)
print("number of hitters in sample: " + str(len(total_r)) + " | min ip " + str(ab_min) + " min qualified starts " + str(min_qualify))

roto_stats = sb.RotoCats()
r_mean, r_sd = sc.eval_m_sd(total_r,"runs")
roto_stats.r.mean = r_mean
roto_stats.r.sd = r_sd
hr_mean, hr_sd = sc.eval_m_sd(total_hr,"hrs")
roto_stats.hr.mean = hr_mean
roto_stats.hr.sd = hr_sd
rbi_mean, rbi_sd = sc.eval_m_sd(total_rbi,"rbis")
roto_stats.rbi.mean = rbi_mean
roto_stats.rbi.sd = rbi_sd
sb_mean, sb_sd = sc.eval_m_sd(total_sb,"sbs")
roto_stats.sb.mean = sb_mean
roto_stats.sb.sd = sb_sd
hoa_mean, hoa_sd = sc.eval_m_sd(total_hoa,"avgs")
roto_stats.avg.mean = league_ba
roto_stats.avg.sd = hoa_sd

#full_player_names = sc.playerFileToList("files/2023_people/hitters_fmt.out")

_,_,_,_,_,bucket_mins, dollar_per_unit = sb.sample_players(player_list, all_player_ats, league_ba, print_players=False, eval_prv=True, ab_min=int(ab_min), roto_stats=roto_stats)

sb.sample_players(people, all_player_ats, league_ba, print_players=True, eval_prv=True, ab_min=int(ab_min), roto_stats=roto_stats, apply_to_all=True, bucket_mins=bucket_mins, dollar_per_unit=dollar_per_unit, to_csv=True)


# load_to_db(all_player_ats)
