from app.database import SessionLocal
from app.models import User

db = SessionLocal()
db.add(User(name="Alice"))
db.add(User(name="Bob"))
db.commit()
db.close()

print("Sample data inserted!")

