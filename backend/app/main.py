from fastapi import FastAPI
from fastapi import HTTPException
from app.api.players import router as players_router
from app.api.games import router as games_router
from app.api.daily_pitcher_stats import router as pitcher_stats_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(players_router)

from fastapi import FastAPI
from app.api.players import router as players_router
from app.api.games import router as games_router
from app.api.daily_pitcher_stats import router as pitcher_stats_router
from app.api.batter_daily_stats import router as batter_stats_router


app = FastAPI()

app.include_router(players_router)
app.include_router(games_router)
app.include_router(pitcher_stats_router)
app.include_router(batter_stats_router)
