from fastapi import FastAPI
from fastapi import HTTPException
from app.api.players import router as players_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app.models import User
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
