python3 -m app.db_io.add_players  ~/retrosheets/2024/2024allplayers.csv
python3 -m app.db_io.import_games  ~/retrosheets/2024/2024pitching.csv ~/retrosheets/2024/2024gameinfo.csv
python3 -m app.db_io.load_pa_stats  ~/retrosheets/2024/2024plays.csv
python3 -m app.db_io.import_fielding  ~/retrosheets/2024/2024fielding.csv
python3 -m app.db_io.import_dhinfo  ~/retrosheets/2024/2024batting.csv
