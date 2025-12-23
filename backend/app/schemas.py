from pydantic import BaseModel

# This is what your API will send to clients
class UserSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # Important: allows SQLAlchemy models to be converted to Pydantic

class UserCreate(BaseModel):
    name: str
