from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from app.base import Base

load_dotenv()  # Load .env first

DATABASE_URL = os.getenv("DATABASE_URL")
print("Database engine using:", DATABASE_URL)  # debug

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


