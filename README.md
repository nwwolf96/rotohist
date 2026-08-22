# rotohist

rotohist is a fantasy-baseball analytics tool built on historical MLB play-by-play data (Retrosheet). It ingests season data into a Postgres database, computes rotisserie-style ("roto") batting and pitching stats and dollar valuations, and exposes the results through a FastAPI backend and a Next.js frontend.

## Project structure

```
.
├── backend/            FastAPI service, data import, and stat-calculation scripts
│   ├── app/
│   │   ├── api/         REST endpoints (players, games, batter/pitcher stats)
│   │   ├── common/      Shared enums, constants, and helpers
│   │   ├── db_calc/     Season/daily stat calculation and roto-value ("auction") engine
│   │   ├── db_io/       Retrosheet CSV importers and DB read/write operations
│   │   ├── models/      SQLAlchemy ORM models
│   │   ├── schemas/     Pydantic response schemas
│   │   ├── database.py  DB engine/session setup (reads DATABASE_URL)
│   │   ├── dependencies.py  FastAPI DB session dependency
│   │   └── main.py      FastAPI app + router registration
│   ├── scripts/         fzf-based interactive viewers for batting/pitching previews
│   ├── years/           Per-year roster files and generated auction-value CSVs
│   ├── load-all.sh      Bulk-imports multiple seasons of Retrosheet data
│   ├── combine_bp.py    Merges batter + pitcher auction rankings into one ranked CSV
│   ├── csv_2_table.py   Pretty-prints a roster CSV/TXT as a table
│   └── requirements.txt
├── frontend/            Next.js (App Router) UI
├── docker-compose.yml   Runs backend + frontend containers together
└── start.sh             Spins up a local Postgres container for development
```

## How it works

1. **Import** — scripts in `backend/app/db_io/` load raw [Retrosheet](https://www.retrosheet.org/) season files (play-by-play, game info, fielding, batting/DH info, player rosters) into Postgres via SQLAlchemy models in `backend/app/models/`.
2. **Calculate** — scripts in `backend/app/db_calc/` (`run_season_batting.py`, `run_season_pitching.py`, and their `daily_*` counterparts) aggregate raw stats over a date range, bucket players by roster slot, compute z-scores against the league sample, and derive rotisserie dollar values.
3. **Serve** — `backend/app/main.py` exposes the data over REST (players, games, batter/pitcher daily and yearly stats).
4. **Display** — the `frontend/` Next.js app fetches from the API and renders it.

## Prerequisites

- Python 3.11+
- Node.js (for the frontend)
- Docker (for Postgres and/or running everything via `docker-compose`)
- Retrosheet season CSVs if you want to (re)populate the database (`load-all.sh` expects them under `~/retrosheets/<year>/`)

## Setup

### 1. Database

Start a local Postgres container:

```bash
./start.sh
```

This runs Postgres 15 in a container named `my-postgres`, mapped to host port `5433`.

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `backend/.env` file with:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/mydb
```

Run the API:

```bash
./run-backend.sh
```

This sets `PYTHONPATH` and starts `uvicorn app.main:app --reload` on `http://localhost:8000`.

Sanity-check the DB connection separately with:

```bash
python test_db.py
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs on `http://localhost:3000` and expects the backend at `http://localhost:8000`.

### 4. Docker Compose (alternative)

To build and run the backend and frontend containers together:

```bash
docker-compose up --build
```

## Loading data

To bulk-import multiple seasons of Retrosheet data (players, games, play-by-play, fielding, DH info) for 2020–2025:

```bash
cd backend
./load-all.sh
```

Each import step can also be run individually, e.g.:

```bash
python3 -m app.db_io.add_players ~/retrosheets/2025/2025allplayers.csv
python3 -m app.db_io.import_games ~/retrosheets/2025/2025pitching.csv ~/retrosheets/2025/2025gameinfo.csv
python3 -m app.db_io.load_pa_stats ~/retrosheets/2025/2025plays.csv
python3 -m app.db_io.import_fielding ~/retrosheets/2025/2025fielding.csv
python3 -m app.db_io.import_dhinfo ~/retrosheets/2025/2025batting.csv
```

## Computing season/daily stats and roto values

Run the season-long batting or pitching valuation over a date range:

```bash
cd backend
python3 -m app.db_calc.run_season_batting --fro <start_date> --to <end_date>
python3 -m app.db_calc.run_season_pitching --fro <start_date> --to <end_date>
```

These scripts write ranked auction-value CSVs (see `backend/years/auction_calc_batter_<year>.csv` and `auction_calc_pitcher_<year>.csv` for examples) and print z-score/roto summaries to the console.

There are also interactive fzf-based previewers:

```bash
cd backend/scripts
./batting_prv.sh <args>
./pitching_prv.sh <args>
```

To merge a batter and pitcher auction-value CSV into one combined, ranked file:

```bash
cd backend
python3 combine_bp.py <batters.csv> <pitchers.csv>
```

This produces `combined_rankings_full.csv`.

To pretty-print a roster file (see `backend/years/2025_rosters/`) as a table:

```bash
cd backend
python3 csv_2_table.py -f <path_to_roster_file>
```

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /players/` | List all players |
| `POST /players/` | Create or update (upsert) a player |
| `GET /games/` | List games, optionally filtered by `year` |
| `GET /games/{gid}` | Get a single game |
| `GET /pitcher-daily-stats/` | Pitcher daily stats, filterable by `game_id`, `player_id`, `year` |
| `GET /batter-daily-stats/` | Batter daily stats, filterable by `playerId`, `gameId` |
| `GET /batter-yearly-stats/` | Batter yearly stats, filterable by `playerId`, `year` |

## Notes

- League configuration (roster slots, team size, position order) for batting and pitching valuations is currently set directly in `run_season_batting.py` / `run_season_pitching.py`.
- `backend/years/2025_rosters/` contains example league roster files in a few different formats, used as input to the auction-value tooling.
