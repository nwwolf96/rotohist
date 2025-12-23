from fastapi import FastAPI
from app.schemas import UserSchema, UserCreate
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.database import SessionLocal
from app.models import User
from app.schemas import UserSchema
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/users", response_model=List[UserSchema])
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users



@app.post("/api/users", response_model=UserSchema)
def create_user(user: UserCreate):
    db = SessionLocal()
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user
