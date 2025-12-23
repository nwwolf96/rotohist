from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()  # load .env from backend folder

DATABASE_URL = os.getenv("DATABASE_URL")
print("Using DATABASE_URL:", DATABASE_URL)  # <-- debug

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchall())
