#!/bin/bash

cd ../ && python3 -m app.db_calc.run_season_batting $* | fzf --header-lines=13 -e --multi --layout=reverse --border=double
