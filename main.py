from fastapi import FastAPI
from sqlmodel import SQLModel, text, Session
from database import engine
from models.user import User

app = FastAPI()

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    result = session.exec(text("SELECT 1"))
    print("DB Connection test:", result.scalar())

# Note: This is just a test to check if the database connection is working. If it works, it'll print a 1.
