#!/bin/bash

cd ../ && python3 -m app.db_calc.run_season_pitching $* | fzf --header-lines=14 -e --multi --layout=reverse --border=double
