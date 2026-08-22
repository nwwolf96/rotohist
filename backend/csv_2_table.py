from tabulate import tabulate
import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-f",
    "--file",
    help="--f --file for file name"
)

args = parser.parse_args()

def loadRosteredFromFile(file, p=True):
    file1 = open(file, "r") 
    all_lines = file1.readlines()
    # header = all_lines[0]
    # print("header is " + str(header))
    player_list = []
    for line_data in all_lines:
        player_list += [line_data.split(",")]
    if p:
        print(tabulate(player_list, headers="firstrow", tablefmt="fancy_grid"))
    return player_list

loadRosteredFromFile(args.file)
