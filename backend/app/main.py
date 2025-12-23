from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import users

app = FastAPI()

# Allow Next.js frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users")
