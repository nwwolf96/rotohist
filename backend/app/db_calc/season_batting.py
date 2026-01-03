from app.models import BatterDailyStats
from sqlalchemy import func
from . import bucket_manager
from . import season_commons 

from tabulate import tabulate

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
]
batting_header_rates = [
    "PA/GP",
    "sta",
    "sit",
    "lSta",
    "lSit",
    "rSta",
    "rSit",
]
batting_header_zscores = [
    "R-Z",
    "HR-Z",
    "RBI-Z",
    "SB-Z",
    "AVG-Z",
    "PRV",
    # "B-POS",
    "PRV-A",
    "Adj-Val",
    "ACV"
]
if season_commons.args.all:
    batting_header_season += batting_header_rates + batting_header_zscores
elif season_commons.args.startsit:
    batting_header_season += batting_header_rates
elif season_commons.args.zscores:
    batting_header_season += batting_header_zscores

class PlayerStarts:
    starts = 0
    sits = 0
    starts_v_left = 0
    sits_v_left = 0
    starts_v_right = 0
    sits_v_right = 0
    total_games_26_man = 0
    left_total_games_26_man = 0
    right_total_games_26_man = 0
    pa_gp = 0.0
    start_rate = 0.0
    sit_rate = 0.0
    start_rate_v_left = 0.0
    sit_rate_v_left = 0.0
    start_rate_v_right = 0.0
    sit_rate_v_right = 0.0

    def __str__(self):
      return str(self.start_rate)+ " " + str(self.starts) + " " + str(self.sit_rate_v_left) + " " + str(self.sit_rate)

class PlayerZScores:
    r = 0.0
    hr = 0.0
    rbi = 0.0
    sb = 0.0
    avg = 0.0
    hoa = 0.0
    total = 0.0

class RotoCats:
    r = season_commons.MSD()
    hr = season_commons.MSD()
    rbi = season_commons.MSD()
    sb = season_commons.MSD()
    avg = season_commons.MSD()

class PlayerAt:
    name = ""
    team = ""
    gp = 0
    batting_order = 0
    hand = ""
    pa = 0
    ab = 0
    h = 0
    r = 0
    hr = 0
    rbi = 0
    bb = 0
    sb = 0
    cs = 0
    avg = 0.0
    pos = ""
    start_stats = PlayerStarts()
    zscores = PlayerZScores()
  
    def __str__(self):
      return str(self.name + " " + str(self.h) + " " + str(self.ab) + " " + str(self.pa))

def getArrayFromAts(p_ats, override=False):
    ret_val = [p_ats.name, p_ats.team, p_ats.gp, p_ats.batting_order, p_ats.hand, p_ats.pa, p_ats.ab, p_ats.h, p_ats.r, p_ats.hr, p_ats.rbi, p_ats.bb, p_ats.sb, p_ats.cs, p_ats.avg, p_ats.pos]
    if override or (season_commons.args.startsit or season_commons.args.all):
        ret_val += [p_ats.start_stats.pa_gp, p_ats.start_stats.start_rate, p_ats.start_stats.sit_rate, p_ats.start_stats.start_rate_v_left, p_ats.start_stats.sit_rate_v_left, p_ats.start_stats.start_rate_v_right, p_ats.start_stats.sit_rate_v_right]
    return ret_val

def loadBatterStatsFromDb(db, player_name, min_qualify):
    filter_result = db.query(BatterDailyStats).filter(BatterDailyStats.playerId == player_name)
    order_mode = []
    positions = {}
    sum_ats = PlayerAt()

    # im doing the below to prevent pyright thinking x might possibly be unbound
    tmp_hand = ""
    tmp_team = ""
    start_stats = PlayerStarts()
    for x in filter_result:
        team = x.player.team
        tmp_hand = str(x.player.bHand).split("Handedness.")[1]
        tmp_team = team
        # if season_commons.args.month != 0 and x.statDate.split("/")[0] != str(season_commons.args.month):
        #     continue
        curr_date = season_commons.dateToNumber(x.gameId[3:])
        if season_commons.dateToNumber(season_commons.args.to) < curr_date or season_commons.dateToNumber(season_commons.args.fro) > curr_date:
            continue
        # Discard all star game
        if team == "AL" or team == "NL":
            continue
        if season_commons.args.startsit or season_commons.args.all:
            if x.bOrder == "0" or "00" not in x.bOrder:
                start_stats.sits += 1
            else:
                start_stats.starts += 1
            #todo implement spAH in my new db
            # if x.spAH == "L":
            #     if x.bOrder == "0" or "00" not in x.bOrder: 
            #         start_stats.sits_v_left += 1
            #     else:
            #         start_stats.starts_v_left += 1
            # elif x.spAH == "R":
            #     if x.bOrder == "0" or "00" not in x.bOrder:
            #         start_stats.sits_v_right += 1
            #     else:
            #         start_stats.starts_v_right += 1
        sum_ats.gp += x.gp
        sum_ats.pa += x.lpa + x.rpa 
        sum_ats.ab += x.lab + x.rab 
        sum_ats.h += x.lb1 + x.rb1 + x.lb2 + x.rb2 + x.lb3 + x.rb3 + x.lhr + x.rhr
        sum_ats.r += x.r
        sum_ats.hr += x.lhr + x.rhr 
        sum_ats.rbi += x.lrbi + x.rrbi 
        sum_ats.bb += x.lbb + x.rbb 
        sum_ats.sb += x.sb
        sum_ats.cs += x.cs
        order_mode += [x.bOrder]
        if x.pos not in positions.keys():
            positions[x.pos] = 1
        else:
            positions[x.pos] += 1
    if int(str(sum_ats.ab)) > 0:
        sum_ats.avg = round(float(sum_ats.h) / float(sum_ats.ab), 3)

    if sum_ats.ab == 0:
        return None
    # print(sum_ats.name + " " + str(sum_ats.ab))
    # print(sum_ats.avg)
    sum_ats.avg = float(f"{sum_ats.avg:.3f}")

    for pos in positions:
        if positions[pos] >= min_qualify:
            if pos == "PH" or pos == "TWP" or pos == "PR":
                continue
            if pos == "C":
                pos = "CC"
            sum_ats.pos += pos + ", "
    # print("positions: 'Pos': GP, | " + str(positions))

    if season_commons.args.startsit or season_commons.args.all:
        start_stats.total_games_26_man = start_stats.starts + start_stats.sits
        start_stats.left_total_games_26_man = start_stats.starts_v_left + start_stats.sits_v_left
        start_stats.right_total_games_26_man = start_stats.starts_v_right + start_stats.sits_v_right
        if sum_ats.gp > 0:
            start_stats.pa_gp = round(float(sum_ats.pa/sum_ats.gp),3)
        else:
            start_stats.pa_gp = 0
        if start_stats.total_games_26_man > 0:
            start_stats.start_rate = round(float(start_stats.starts/start_stats.total_games_26_man),3)
        else:
            start_stats.start_rate = 0
        if start_stats.total_games_26_man > 0:
            start_stats.sit_rate = round(float(start_stats.sits/start_stats.total_games_26_man),3)
        else:
            start_stats.sit_rate = 0
        if start_stats.left_total_games_26_man> 0:
            start_stats.start_rate_v_left = round(float(start_stats.starts_v_left/start_stats.left_total_games_26_man),3)
        else:
            start_stats.start_rate_v_left = 0
        if start_stats.left_total_games_26_man> 0:
            start_stats.sit_rate_v_left = round(float(start_stats.sits_v_left/start_stats.left_total_games_26_man),3)
        else:
            start_stats.sit_rate_v_left = 0
        if start_stats.right_total_games_26_man> 0:
            start_stats.start_rate_v_right = round(float(start_stats.starts_v_right/start_stats.right_total_games_26_man),3)
        else:
            start_stats.start_rate_v_right = 0
        if start_stats.right_total_games_26_man> 0:
            start_stats.sit_rate_v_right= round(float(start_stats.sits_v_right/start_stats.right_total_games_26_man),3)
        else:
            start_stats.sit_rate_v_right= 0
    order_mode_mode = max(set(order_mode), key=order_mode.count)
    sum_ats.name = player_name
    sum_ats.batting_order = order_mode_mode

    # im doing the below to prevent pyright thinking x might possibly be unbound
    sum_ats.team = tmp_team
    sum_ats.hand = tmp_hand
    if season_commons.args.startsit or season_commons.args.all:
        sum_ats.start_stats = start_stats
    return sum_ats

def cut_positions(player_list):
    player_names = []
    # print("player list is " + str(player_list))
    for player_name,_ in player_list:
        player_names += [player_name]
    return player_names 

def get_league_ba(player_list, all_player_ats, ab_min=100):
    abs = []
    hs = []
    for person,_ in player_list:
        p_ats = all_player_ats[person]
        # print("player is " + str(person) + " " + str(p_ats))
        if p_ats == None:
            continue
        if p_ats.ab < ab_min:
            # drop from the sample, don't like small samplers
            continue
        hs += [p_ats.h]
        abs += [p_ats.ab]
    league_ba = sum(hs) / sum(abs)
    print("League avg " + str(league_ba))
    return league_ba

def evaluate_zs(roto_stats, p_ats, ret_val, override=False):
    r_z = (float(p_ats.r)-roto_stats.r.mean)/roto_stats.r.sd
    hr_z = (float(p_ats.hr)-roto_stats.hr.mean)/roto_stats.hr.sd
    rbis_z = (float(p_ats.rbi)-roto_stats.rbi.mean)/roto_stats.rbi.sd
    if roto_stats.sb.sd != 0:
        sbs_z = (float(p_ats.sb)-roto_stats.sb.sd)/roto_stats.sb.sd
    else:
        sbs_z = 0
    # hoa = float(p_ats.h)-(float(p_ats.ab)*league_ba)
    hoa_r = (float(p_ats.h) - roto_stats.avg.mean * float(p_ats.ab)) / roto_stats.avg.sd
    tot = r_z + hr_z + rbis_z + sbs_z + hoa_r
    if override or (season_commons.args.all or season_commons.args.zscores):
        p_ats.zscores.r   = round(r_z,3)
        p_ats.zscores.hr   = round(hr_z,3)
        p_ats.zscores.rbi  = round(rbis_z,3)
        p_ats.zscores.sb   = round(sbs_z,3)
        p_ats.zscores.hoa  = round(hoa_r,3)
        p_ats.zscores.total = round(tot,3)
        ret_val += [p_ats.zscores.r,p_ats.zscores.hr,p_ats.zscores.rbi,p_ats.zscores.sb,p_ats.zscores.hoa,p_ats.zscores.total] #uncomment if you want to show came from bucket, str(bucket_pos)]

def assign_dh_magic_val(bucket_mins):
    max_buc = ("",float(-100.0))
    for k in bucket_mins.keys():
        if bucket_mins[k][1] > 0:
            bucket_mins[k] = (bucket_mins[k][0],0)
        if bucket_mins[k][1] > max_buc[1]:
            max_buc = (k,bucket_mins[k][1])
    bucket_mins["DH"] = ("Magic Adjustment", max_buc[1] * 0.75)

def adjust_prvs(bucket_mins, totals, apply_to_all, dollar_per_unit):
    ct = 0
    batter_tv = 0.0
    for ret_val in totals:
        player_pos = ret_val[15]
        player_prv = ret_val[-1]
        min_val = ("",0)
        for pos in player_pos.split(", "):
            if (pos == "RF" or pos == "CF" or pos == "LF"):
                pos = "OF"
            elif (pos == "P" or pos == "" or pos == "IF"):
                continue
            if bucket_mins[pos][1] < min_val[1]:
                min_val = (pos,bucket_mins[pos][1])
        adj_val = float(min_val[1])

        if adj_val < 0:
            adj_val *= -1
        batter_tv += player_prv + adj_val
        totals[ct] += [player_prv + adj_val, adj_val]
        if apply_to_all:
            totals[ct] += [(player_prv + adj_val) * dollar_per_unit]
        ct += 1
    total_money = 2844.0
    projected_pitcher_tv = .35 * batter_tv
    if not apply_to_all:
        print("total units in sample is | " + str(batter_tv) + " | total dollars | " + str(total_money)+ " | dollars per unit " + str(total_money/(batter_tv+projected_pitcher_tv)))
    return float(total_money/(batter_tv+projected_pitcher_tv))

def sample_players(player_list, all_player_ats, league_ba, print_players=True, eval_prv=True, ab_min=100, roto_stats=None, apply_to_all=False, bucket_mins=None, dollar_per_unit=None, to_csv=False, override=False):
    totals = []
    abs = []
    hs = []
    rs = []
    hrs = []
    rbis = []
    sbs = []
    hoas = []
    # dollar_per_unit = None
    if bucket_mins == None:
        bucket_mins = {}
    for list_item in player_list:
        if not isinstance(list_item, tuple):
            person = list_item
            bucket_pos = "Unwash"
        else:
            person,bucket_pos = list_item
        p_ats = all_player_ats[person]
        if p_ats == None:
            continue
        ret_val = getArrayFromAts(p_ats)
        if p_ats.ab < ab_min:
            continue
        if eval_prv and roto_stats != None:
            evaluate_zs(roto_stats, p_ats, ret_val, override)
            if not apply_to_all:
                season_commons.fill_bucket_mins(bucket_mins, bucket_pos, person, p_ats)
        totals += [ret_val]
        hoa = float(p_ats.h)-(float(p_ats.ab)*league_ba)
        hs += [p_ats.h]
        abs += [p_ats.ab]
        rs += [p_ats.r]
        hrs += [p_ats.hr]
        rbis += [p_ats.rbi]
        sbs += [p_ats.sb]
        hoas += [hoa]
    if override or (eval_prv and (season_commons.args.all or season_commons.args.zscores)):
        if not apply_to_all:
            assign_dh_magic_val(bucket_mins)
        dollar_per_unit = adjust_prvs(bucket_mins, totals, apply_to_all, dollar_per_unit)
    if print_players:
        if override:
            header = [
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
                "PRV",
                # "B-POS",
                "PRV-A",
                "Adj-Val",
                "ACV"
            ]
            totals.sort(
                key=lambda row: (row[header.index("ACV")]), reverse=(True)
            )
            ct = 0
            for x in totals:
                totals[ct] = [ct+1] + x
                ct += 1
            # batting_header_season= ["Rank"] + batting_header_season
            totals = [header] + totals
        else:
            totals.sort(
                key=lambda row: (row[batting_header_season.index(season_commons.args.sort)]), reverse=(not season_commons.args.reverse)
            )
            ct = 0
            for x in totals:
                totals[ct] = [ct+1] + x
                ct += 1
            # batting_header_season= ["Rank"] + batting_header_season
            totals = [batting_header_season] + totals
        if to_csv:
            filename = "2023_auction_calc_batter.csv"
            with open(filename, "w") as f:
                f.write(",")
                for row in totals:
                    for col in row:
                        item = str(col)
                        f.write(item.replace(",","|") + ",")
                    f.write("\n")
                
        print(tabulate(totals, headers="firstrow", tablefmt="fancy_grid"))
    return (rs, hrs, rbis, sbs, hoas, bucket_mins, dollar_per_unit)


def fill_buckets(player_ats_list, team_size, pos_ct, pos_order):
    bm = bucket_manager.BucketManager(pos_order)
    for _,p_ats in player_ats_list.items():
        if p_ats == None:
            continue
        pos = p_ats.pos.split(", ")
        name = p_ats.name
        # TODO, write function to make this dynamic
        val = p_ats.r
        of_not_hit = True
        b13_not_hit = True
        b2s_not_hit = True
        if pos == "" or pos == "P":
            continue
        for p in pos:
            if (p == "RF" or p == "CF" or p == "LF"):
                p = "OF"
                if of_not_hit:
                    of_not_hit = False
                else:
                    continue
            if (p == "2B" or p == "SS") and b2s_not_hit:
                bm.add_player(name, p, val)
                p = "2BorSS"
                b2s_not_hit = False
            if (p == "1B" or p == "3B") and b13_not_hit:
                bm.add_player(name, p, val)
                p = "1Bor3B"
                b13_not_hit = False
            if p == "DH" or p == "" or p == "P" or p == "IF":
                continue
            bm.add_player(name, p, val)
        # read the player to the utility bucket
        bm.add_player(name, "UTIL", val)
    ct = 0
    player_names = []
    for pos in pos_order:
        while pos_ct[pos] > 0:
            player_list = bm.empty_bucket(pos,team_size)
            # player_names += player_list
            for player,_ in player_list:
                player_names += [(player,pos)]
            ct += 1
            pos_ct[pos] -= 1
    return player_names

#todo load to the database
# def load_to_db(all_player_ats):
#     for _,ats in all_player_ats.items():
#         filter_result = 0
#         try:
#             filter_result = SeasonBatting.objects.filter(name=ats.name,h=ats.h).update(
#                 team=ats.team,
#                 gp=ats.gp,
#                 bo=ats.batting_order,
#                 l_r=ats.hand,
#                 pa=ats.pa,
#                 ab=ats.ab,
#                 h=ats.h,
#                 r=ats.r,
#                 hr=ats.hr,
#                 rbi=ats.rbi,
#                 bb=ats.bb,
#                 sb=ats.sb,
#                 cs=ats.cs,
#                 avg=ats.avg,
#                 pos=ats.pos,
#                 pa_gp=ats.start_stats.pa_gp,
#                 sta=ats.start_stats.start_rate,
#                 sit=ats.start_stats.sit_rate,
#                 lSta=ats.start_stats.start_rate_v_left,
#                 lSit=ats.start_stats.sit_rate_v_left,
#                 rSta=ats.start_stats.start_rate_v_right,
#                 rSit=ats.start_stats.sit_rate_v_right,
#                 r_z=ats.zscores.r,
#                 hr_z=ats.zscores.hr,
#                 rbi_z=ats.zscores.rbi,
#                 sb_z=ats.zscores.sb,
#                 avg_z=ats.zscores.avg,
#                 prv=ats.zscores.total
#             )
#             # print("updated stats for " + ats.name)
#             # print("filter status is " + str(filter_result))
#         except:
#             SeasonBatting.objects.create(
#                 name=ats.name,
#                 team=ats.team,
#                 gp=ats.gp,
#                 bo=ats.batting_order,
#                 l_r=ats.hand,
#                 pa=ats.pa,
#                 ab=ats.ab,
#                 h=ats.h,
#                 r=ats.r,
#                 hr=ats.hr,
#                 rbi=ats.rbi,
#                 bb=ats.bb,
#                 sb=ats.sb,
#                 cs=ats.cs,
#                 avg=ats.avg,
#                 pos=ats.pos,
#                 pa_gp=ats.start_stats.pa_gp,
#                 sta=ats.start_stats.start_rate,
#                 sit=ats.start_stats.sit_rate,
#                 lSta=ats.start_stats.start_rate_v_left,
#                 lSit=ats.start_stats.sit_rate_v_left,
#                 rSta=ats.start_stats.start_rate_v_right,
#                 rSit=ats.start_stats.sit_rate_v_right,
#                 r_z=ats.zscores.r,
#                 hr_z=ats.zscores.hr,
#                 rbi_z=ats.zscores.rbi,
#                 sb_z=ats.zscores.sb,
#                 avg_z=ats.zscores.avg,
#                 prv=ats.zscores.total
#             )
#             print("created player stats for " + ats.name)
#         if (filter_result == 0):
#             SeasonBatting.objects.create(
#                 name=ats.name,
#                 team=ats.team,
#                 gp=ats.gp,
#                 bo=ats.batting_order,
#                 l_r=ats.hand,
#                 pa=ats.pa,
#                 ab=ats.ab,
#                 h=ats.h,
#                 r=ats.r,
#                 hr=ats.hr,
#                 rbi=ats.rbi,
#                 bb=ats.bb,
#                 sb=ats.sb,
#                 cs=ats.cs,
#                 avg=ats.avg,
#                 pos=ats.pos,
#                 pa_gp=ats.start_stats.pa_gp,
#                 sta=ats.start_stats.start_rate,
#                 sit=ats.start_stats.sit_rate,
#                 lSta=ats.start_stats.start_rate_v_left,
#                 lSit=ats.start_stats.sit_rate_v_left,
#                 rSta=ats.start_stats.start_rate_v_right,
#                 rSit=ats.start_stats.sit_rate_v_right,
#                 r_z=ats.zscores.r,
#                 hr_z=ats.zscores.hr,
#                 rbi_z=ats.zscores.rbi,
#                 sb_z=ats.zscores.sb,
#                 avg_z=ats.zscores.avg,
#                 prv=ats.zscores.total
#             )
#             print("created player stats for " + ats.name)
