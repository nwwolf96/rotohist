import argparse
import concurrent.futures
from sqlalchemy import func

from enum import Enum
from app.models import BatterDailyStats, PitcherDailyStats

MONTH_LIST = [31,28,31,30,31,30,31,31,30,31,30,31]

class PlayerType(Enum):
    PITCHER = "Pitcher"
    HITTER = "Hitter"

parser = argparse.ArgumentParser()

parser.add_argument(
    "-s", "--sort", dest="sort", default="HR", help="Argument to sort data on"
)
parser.add_argument(
    "-f",
    "--from",
    dest="fro",
    default="03/30/2023",
    help="-f or --from to provide a start date for the sample",
)
parser.add_argument(
    "-t",
    "--to",
    dest="to",
    default="10/04/2023",
    help="-t or --to to provide an end date for the sample",
)
parser.add_argument(
    "-r",
    "--reverse",
    dest="reverse",
    action="store_true",
    help="Argument to sort data on (reverse order)",
)
parser.add_argument(
    "-q",
    "--qualified",
    dest="qualified",
    action="store_true",
    help="-q or --qualified filters for qualified hitters",
)
parser.add_argument(
    "-ss",
    "--startsit",
    dest="startsit",
    action="store_true",
    help="-ss or --startsit filters for start v sit percentages (only works for batters, for pitchers this is ignored)",
)
parser.add_argument(
    "-z",
    "--zscores",
    dest="zscores",
    action="store_true",
    help="-z or --zscores to filter zscore values",
)
parser.add_argument(
    "-a",
    "--all",
    dest="all",
    action="store_true",
    help="-a or --all to get all batter stats",
)

parser.add_argument(
    "-b",
    "--base",
    dest="base",
    action="store_true",
    help="-b or --base to get base batter stats",
)

args = parser.parse_args()

class MSD:
    mean = 0.0
    sd = 0.0

def get_pitchers():
    ran = get_date_range(3,30,10,1,2023)
    pitchers = []
    for x in ran:
        date_str = "" + str(x.month) + "/" + str(x.day) + "/" + str(x.year)
        filtered_result = DailyPitchingStats.objects.filter(statDate=date_str)
        for x in filtered_result:
            if x.name not in pitchers:
                pitchers += [x.name]
    return pitchers

def write_pitchers_to_file(player_names):
    filename = "2023_people/pitchers_fmt.out"
    with open(filename, "w") as f:
        for name in player_names:
            f.write(name.replace(" ","_") + "\n")

def playerFileToList(player_file):
    file1 = open(player_file, "r") 
    player_list = []
    for person in file1.readlines():
        person = person.replace("\n","").replace("_"," ")
        player_list += [(person, "Unwash")]
    return player_list

def dateToNumber(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    month = int(month)
    day = int(day)
    year = int(year)
    magic_num = sum(MONTH_LIST[0:month])
    return (magic_num + day) + (year * 365.25)

# load the player data for every player in the player file. Uses the func function to load every 
# player from db. Returns a dictionary of the player name -> db lookup data
def load_names_from_year(db, startDate,endDate,type):
    if startDate[0] == "0":
        startDate = startDate[1:]
    if endDate[0] == "0":
        endDate = endDate[1:]
    if(type == PlayerType.HITTER):
        filter_result = (
            db.query(PitcherDailyStats)
            .filter(func.substr(PitcherDailyStats.gameId, 4, 8) >= startDate)
            .filter(func.substr(PitcherDailyStats.gameId, 4, 8) <= endDate)
            .all()
        )
    else:
        filter_result = (
            db.query(BatterDailyStats)
            .filter(func.substr(BatterDailyStats.gameId, 4, 8) >= startDate)
            .filter(func.substr(BatterDailyStats.gameId, 4, 8) <= endDate)
            .all()
        )
    all_names = []
    for x in filter_result:
        if x.playerId not in all_names:
            all_names += [x.playerId]
    return all_names

# load the player data for every player in the player file. Uses the func function to load every 
# player from db. Returns a dictionary of the player name -> db lookup data
def load_all_ats(db, people_list, min_qualify, func):
    ats = {}
    thread_contents = {}
    # splits the db loading for all players into 5 worker threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for person in people_list:
            # person = person.replace("\n","").replace("_"," ")
            thread_contents[executor.submit(func, db, person, min_qualify)] = person
        for future in concurrent.futures.as_completed(thread_contents):
            person = thread_contents[future]
            try:
                ats[person] = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (person, exc))
                quit(1)
    return ats

# load the player data for every player in the player file. Uses the func function to load every 
# player from db. Returns a dictionary of the player name -> db lookup data
def get_names_from_file(player_file):
    people = []
    file1 = open(player_file, "r") 
    for person in file1.readlines():
        person = person.replace("\n","").replace("_"," ")
        people += [person]
    return people 

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

def fill_bucket_mins(bucket_mins, bucket_pos, person, p_ats):
    if bucket_pos == "1Bor3B" or bucket_pos == "2BorSS" or bucket_pos == "UTIL" or bucket_pos == "OF": 
        for pos in p_ats.pos.split(", "):
            if (pos == "RF" or pos == "CF" or pos == "LF"):
                pos = "OF"
            if pos == "DH" or pos == "" or pos == "P":
                continue
            if pos not in bucket_mins.keys():
                bucket_mins[pos] = (person, p_ats.zscores.total)
            elif bucket_mins[pos][1] > p_ats.zscores.total: 
                bucket_mins[pos] = (person, p_ats.zscores.total)
    else:
        if bucket_pos not in bucket_mins.keys():
            bucket_mins[bucket_pos] = (person, p_ats.zscores.total)
        elif bucket_mins[bucket_pos][1] > p_ats.zscores.total: 
            bucket_mins[bucket_pos] = (person, p_ats.zscores.total)

def eval_m_sd(data_array, category):
    mean = sum(data_array) / len(data_array) 
    variance = sum([((x - mean) ** 2) for x in data_array]) / len(data_array) 
    sd = variance ** 0.5
    print("mean of " + category + ": " + str(round(mean,3)) + "\t| std of w " + category + ": " + str(round(sd,3)))
    return mean, sd


def adj_val(bucket_mins):
    max_buc = ("",float(-100.0))
    for k in bucket_mins.keys():
        if bucket_mins[k][1] > 0:
            bucket_mins[k][1] = 0
        if bucket_mins[k][1] > max_buc[1]:
            max_buc = (k,bucket_mins[k][1])
        #print("bucket min for " + str(k) + " is " + str(bucket_mins[k]))
