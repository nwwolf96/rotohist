from app.models import PitcherDailyStats
from sqlalchemy import func
from . import bucket_manager
from . import season_commons 

from tabulate import tabulate

pitching_header_season = [
    "Name", 
    "Team", 
    "L/R", 
    "POS",
    "IP", 
    "GS", 
    "GP", 
    "HA", 
    "R", 
    "ER", 
    "HR", 
    "BB", 
    "K", 
    "QS", 
    "W", 
    "L", 
    "S", 
    "HD", 
    "BS", 
    "ERA", 
    "WHIP", 
    "SB",
    "CS",
    "SBP",
    # TODO add back in if i want these stats
    # "NP", 
    # "Strk", 
    # "Ball", 
]
pitching_header_zscores = [
    "W-Z",
    "K-Z",
    "S-Z",
    "ERA-Z",
    "WHIP-Z",
    "Z-SUM",
    "Z-SUM-A",
    "ACV"
]
if season_commons.args.all or season_commons.args.zscores:
    pitching_header_season += pitching_header_zscores

class PitcherZScores:
    w = 0.0
    k = 0.0
    s = 0.0
    eroa = 0.0
    whoa = 0.0
    total = 0.0

class RotoCats:
    w = season_commons.MSD()
    k = season_commons.MSD()
    s = season_commons.MSD()
    era = season_commons.MSD()
    whip = season_commons.MSD()

class PitcherAt:
    name = ""
    team = ""
    hand = ""
    pos = ""
    ip = 0.0
    gs = 0
    gp = 0
    ha = 0
    r = 0
    er = 0
    hr = 0
    bb = 0
    k = 0
    qs = 0
    w = 0
    l = 0
    s = 0
    hd = 0
    bs = 0
    era = ""
    whip = "" 
    sb = 0
    cs = 0
    sbp = 0.0
    np = 0
    strike = 0
    ball = 0
    zscores = PitcherZScores()
  
    def __str__(self):
      return str(self.name + " " + str(self.ip) + " " + str(self.w) + " " + str(self.k))

def getArrayFromPats(pats):
    ret_val = [pats.name, pats.team, pats.hand, pats.pos, pats.ip, pats.gs, pats.gp, pats.ha, pats.r, pats.er, pats.hr, pats.bb, pats.k, pats.qs, pats.w, pats.l, pats.s, pats.hd, pats.bs, pats.era, pats.whip, pats.sb, pats.cs, pats.sbp] # TODO add these back in if care, pats.np, pats.strike, pats.ball]
    return ret_val

def loadPitcherStatsFromDb(db, player_name, min_qualify=3):
    filter_result = db.query(PitcherDailyStats).filter(PitcherDailyStats.playerId == player_name)
    positions = []
    sum_pats = PitcherAt()
    ip_chunks = 0
    tmp_hand = ""
    tmp_team = ""
    for x in filter_result:
        team = x.player.team
        teams = team.split(",")
        tmp_team = ""
        for team in teams: 
            if tmp_team == "":
                tmp_team += team
            if team not in tmp_team:
                tmp_team += ", " + team 
        tmp_hand = str(x.player.tHand).split("Handedness.")[1]
        curr_date = season_commons.dateToNumber(x.gameId[3:])
        if season_commons.dateToNumber(season_commons.args.to) < curr_date or season_commons.dateToNumber(season_commons.args.fro) > curr_date:
            continue
        # Discard all star game
        if x.team == "AL" or x.team == "NL":
            continue
        sum_pats.gs += int(x.gs)
        sum_pats.gp += 1
        sum_pats.ip += float(x.outs/3)
        sum_pats.ha += int(x.ha)
        sum_pats.r += int(x.r)
        sum_pats.er += int(x.er)
        sum_pats.hr += int(x.hr)
        sum_pats.bb += int(x.bb)
        sum_pats.k += int(x.k)
        sum_pats.qs += int(x.qs)
        sum_pats.w += int(x.win_p)
        sum_pats.l += int(x.lose_p)
        sum_pats.s += int(x.sv)
        sum_pats.sb += int(x.sb)
        sum_pats.cs += int(x.cs)
        if round(float(sum_pats.ip)%1,3) == 0.1:
            sum_pats.ip -= .1
            ip_chunks += 1
        elif round(float(sum_pats.ip)%1,3) == 0.2:
            sum_pats.ip -= .2
            ip_chunks += 2

    # if sum_pats.np > 0:
    sum_pats.era, sum_pats.whip = season_commons.calc_era_whip(sum_pats.ip, ip_chunks, sum_pats.er, sum_pats.bb, sum_pats.ha)
    whole_ip = sum_pats.ip + .333333 * ip_chunks
    sum_pats.ip = whole_ip
    if (sum_pats.ip > 0.0):
        sum_pats.sbp = round(sum_pats.sb / sum_pats.ip,3)
    sum_pats.name = player_name
    
    # im doing the below to prevent pyright thinking x might possibly be unbound
    sum_pats.team = tmp_team
    sum_pats.hand = tmp_hand
    if sum_pats.gs >= min_qualify:
        positions += ["SP"]
    if (sum_pats.gp - sum_pats.gs) >= min_qualify:
        positions += ["RP"]
    if len(positions) == 0:
        positions += ["P"]
    for pos in positions:
        if sum_pats.pos == "":
            sum_pats.pos += pos
            continue
        sum_pats.pos += ", " + pos 
    return sum_pats

def get_league_era_whip(player_list, all_pitcher_ats, ip_min=100):
    er = 0.0
    bb = 0.0
    h  = 0.0
    ip = 0.0
    for person,_ in player_list:
        pats = all_pitcher_ats[person]
        if pats == None:
            continue
        if pats.ip < ip_min:
            # drop from the sample, don't like small samplers
            continue
        er += pats.er
        h  += pats.ha
        bb += pats.bb
        ip += pats.ip
    era,whip =  season_commons.calc_era_whip(ip,0,er,bb,h)
    print("League era " + str(era) + " | league whip " + str(whip))
    return era,whip

def evaluate_zs(roto_stats, pats, ret_val):
    w_z = (float(pats.w)-roto_stats.w.mean)/roto_stats.w.sd
    k_z = (float(pats.k)-roto_stats.k.mean)/roto_stats.k.sd
    s_z = (float(pats.s)-roto_stats.s.mean)/roto_stats.s.sd
    # eroa = (float(pats.er)*9)-(league_era*pats.ip)
    # whoa = (float(pats.bb)+float(pats.ha))-(float(pats.ip)*league_whip)
    era_z = -((float(pats.er)*9)-(float(roto_stats.era.mean)*pats.ip)) / roto_stats.era.sd
    whip_z = -((float(pats.bb)+float(pats.ha))-(float(pats.ip)*float(roto_stats.whip.mean))) / roto_stats.whip.sd
    tot = w_z + k_z + s_z + era_z + whip_z
    if season_commons.args.all or season_commons.args.zscores:
        pats.zscores.w     = round(w_z,3)
        pats.zscores.k     = round(k_z,3)
        pats.zscores.s     = round(s_z,3)
        pats.zscores.eroa  = round(era_z,3)
        pats.zscores.whoa  = round(whip_z,3)
        pats.zscores.total = round(tot,3)
        ret_val += [pats.zscores.w,pats.zscores.k,pats.zscores.s,pats.zscores.eroa, pats.zscores.whoa,pats.zscores.total] #uncomment if you want to show came from bucket str(bucket_pos)]

def adjust_prvs(bucket_mins, totals, apply_to_all, dollar_per_unit):
    ct = 0
    pitcher_tv = 0.0
    min_adj = 0
    for _,(_,adj) in bucket_mins.items():
        if adj < min_adj:
            min_adj = adj
    for ret_val in totals:
        player_prv = ret_val[-1]

        # For pitchers, there is no need to adjust per position, for it devalues relievers. Therefore, we just
        # get the minimum overall pitcher to get auction calculateor values 
        if min_adj < 0:
            min_adj *= -1
        adj_val = min_adj
        pitcher_tv += player_prv + adj_val
        totals[ct] += [player_prv + adj_val]
        if apply_to_all:
            totals[ct] += [(player_prv + adj_val) * dollar_per_unit]
        # print("adjustment for " + player_name + " is " + str(pitcher_tv)) 
        ct += 1
    total_money = 2844.0
    projected_batter_tv = .65 * pitcher_tv
    if not apply_to_all:
        print("total units in sample is | " + str(pitcher_tv) + " | total dollars | " + str(total_money)+ " | dollars per unit " + str(total_money/(pitcher_tv+projected_batter_tv)))
    return float(total_money/(pitcher_tv+projected_batter_tv))

def sample_players(player_list, all_pitcher_ats, league_era, league_whip, print_players=True, eval_prv=True, ip_min=100, roto_stats=None, apply_to_all=False, bucket_mins=None, dollar_per_unit=None, to_csv=False, db=None):
    totals = []
    w = []
    k = []
    s = []
    eroas = []
    whoas = []
    if bucket_mins == None:
        bucket_mins = {}
    for list_item in player_list:
        if not isinstance(list_item, tuple):
            person = list_item
            bucket_pos = "Unwash"
        else:
            person,bucket_pos = list_item

        pats = all_pitcher_ats[person]
        if pats == None:
            continue
        ret_val = getArrayFromPats(pats)
        if pats.ip < ip_min:
            # drop from the sample, don't like small samplers
            continue
        if eval_prv:
            evaluate_zs(roto_stats, pats, ret_val)
            if not apply_to_all:
                season_commons.fill_bucket_mins(bucket_mins, bucket_pos, person, pats)
        totals += [ret_val]
        # hoa = float(p_ats.h)-(float(p_ats.ab)*league_ba)
        # era = round(float(er)/float(whole_ip)*9.0,4)
        # whip = round((float(bb)+float(ha))/(whole_ip),4)
        eroa = (float(pats.er)*9)-(league_era*pats.ip)
        whoa = (float(pats.bb)+float(pats.ha))-(float(pats.ip)*league_whip)
        # print("er is " + str(pats.er) + " ip is " + str(float(pats.ip)) + " era is " + str(league_era) + " | " + str(eroa) + " | " + str(whoa))
        w += [pats.w]
        k += [pats.k]
        s += [pats.s]
        eroas += [eroa]
        whoas += [whoa]
    if eval_prv and (season_commons.args.all or season_commons.args.zscores):
        dollar_per_unit = adjust_prvs(bucket_mins, totals, apply_to_all, dollar_per_unit)
    if print_players:
        totals.sort(
            key=lambda row: (row[pitching_header_season.index(season_commons.args.sort)]), reverse=(not season_commons.args.reverse)
        )
        ct = 0
        for x in totals:
            if db != None:
                x[0] = season_commons.lookup_id_to_name(db, x[0])
            totals[ct] = [ct+1] + x
            ct += 1
        totals = [pitching_header_season] + totals
        if to_csv:
            filename = "auction_calc_pitcher.csv"
            with open(filename, "w") as f:
                f.write(",")
                for row in totals:
                    for col in row:
                        item = str(col)
                        f.write(item.replace(",","|") + ",")
                    f.write("\n")
                
        print(tabulate(totals, headers="firstrow", tablefmt="fancy_grid"))
    return (w, k, s, eroas, whoas, bucket_mins, dollar_per_unit)

def fill_buckets(player_ats_list, team_size, pos_ct, pos_order):
    bm = bucket_manager.BucketManager(pos_order)
    for _,p_ats in player_ats_list.items():
        if p_ats == None:
            continue
        pos = p_ats.pos.split(", ")
        name = p_ats.name
        # TODO, write function to make this dynamic
        val_sp = p_ats.k
        val_rp = p_ats.s
        for p in pos:
            if p == "SP":
                bm.add_player(name, p, val_sp)
            if p == "RP":
                bm.add_player(name, p, val_rp)
            if p == "" or p == "P":
                continue
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

