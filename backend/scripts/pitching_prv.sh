#!/bin/bash

cd ../ && python3 -m app.db_calc.run_season_pitching $* | fzf --header-lines=12 -e --multi --layout=reverse --border=double
