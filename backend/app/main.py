from fastapi import FastAPI
from app.database import SessionLocal
from app.models import User
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

