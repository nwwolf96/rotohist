from dotenv import load_dotenv
import os
from app.database import Base, engine
from app.models import User

# Load environment variables from .env
load_dotenv()

print("Using DATABASE_URL:", os.getenv("DATABASE_URL"))  # debug

# Create tables
Base.metadata.create_all(bind=engine)
print("Tables created!")

