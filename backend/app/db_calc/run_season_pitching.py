import app.db_calc.season_pitching as sp
import app.db_calc.season_commons as sc
from app.database import SessionLocal

TOTAL_DAYS_SEASON = 186
ip_min = 10
min_qualify = 3

total_days = sc.dateToNumber(sc.args.to)-sc.dateToNumber(sc.args.fro)
if total_days > TOTAL_DAYS_SEASON:
    total_days = TOTAL_DAYS_SEASON

min_qualify = min_qualify*(total_days/TOTAL_DAYS_SEASON)
ip_min = ip_min*(total_days/TOTAL_DAYS_SEASON)

print("Sample from " + sc.args.fro + " to " + sc.args.to + " | total days: " + str(total_days))

TEAM_SIZE = 15
POS_CT = {"SP": 7, "RP": 2}
AUCT_POS = {"SP": "K", "RP": "S"}
POS_ORDER = ["SP","RP"]

# ip_min = 10
# min_qualify = 3

NAMES_FROM_FILE = False

db = SessionLocal()

# TODO fix this... this is a bit of a hack, i need to change the db to store the date value that I calculated in commons
if "10/" in sc.args.to:
    people = sc.get_names_from_file("files/2023_people/pitchers_fmt.out")
    all_pitcher_ats = sc.load_all_ats(db, people, min_qualify, sp.loadPitcherStatsFromDb)
else:
    print("from is " + sc.args.fro + " + "  + sc.args.to)
    people = sc.load_names_from_year(db, sc.args.fro, sc.args.to, sc.PlayerType.PITCHER)
    all_pitcher_ats = sc.load_all_ats(db, people, min_qualify, sp.loadPitcherStatsFromDb)
# full_player_names = get_pitchers()
# write_pitchers_to_file(full_player_names)
# full_player_names = playerFileToList("../files/2023_people/pitchers_fmt.out")
# people = load_names_from_year(sc.args.fro, sc.args.to, sc.PlayerType.PITCHER)
# all_pitcher_ats = sc.load_all_ats(people, min_qualify, sp.loadPitcherStatsFromDb)

player_list = sp.fill_buckets(all_pitcher_ats, TEAM_SIZE, POS_CT, POS_ORDER)
# print("player list buckets is " + str(player_list))
league_era, league_whip = sp.get_league_era_whip(player_list, all_pitcher_ats, int(ip_min))
(w,k,s,eroas,whoas,_,_) = sp.sample_players(player_list, all_pitcher_ats, float(league_era), float(league_whip), print_players=False, ip_min=int(ip_min), eval_prv=False)
print("number of pitchers in sample: " + str(len(k)) + " | min ip " + str(ip_min) + " min qualified starts " + str(min_qualify))

roto_stats = sp.RotoCats()
ws_mean, ws_sd = sc.eval_m_sd(w,"wins")
roto_stats.w.mean = ws_mean
roto_stats.w.sd = ws_sd
ks_mean, ks_sd = sc.eval_m_sd(k,"ks")
roto_stats.k.mean = ks_mean
roto_stats.k.sd = ks_sd
svs_mean, svs_sd = sc.eval_m_sd(s,"saves")
roto_stats.s.mean = svs_mean
roto_stats.s.sd = svs_sd
eroas_mean, eroas_sd = sc.eval_m_sd(eroas,"era")
roto_stats.era.mean = float(league_era)
roto_stats.era.sd = eroas_sd
whoas_mean, whoas_sd = sc.eval_m_sd(whoas,"whip")
roto_stats.whip.mean = float(league_whip)
roto_stats.whip.sd = whoas_sd

_,_,_,_,_,bucket_mins, dollar_per_unit = sp.sample_players(player_list, all_pitcher_ats, float(league_era), float(league_whip), print_players=False, eval_prv=True, ip_min=int(ip_min), roto_stats=roto_stats)

sp.sample_players(people, all_pitcher_ats, float(league_era), float(league_whip), print_players=True, eval_prv=True, ip_min=int(ip_min), roto_stats=roto_stats, apply_to_all=True, bucket_mins=bucket_mins, dollar_per_unit=dollar_per_unit, to_csv=True, db=db)
