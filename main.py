from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, text, Session
from database import engine
from models.user import User
from models.skill import Skill
from models.user_skill import UserSkill
from models.project import Project
from models.project_role import ProjectRole
# from models.application import Application
from routers.auth import router as auth_router
from security.jwt import get_current_user

app = FastAPI()
app.include_router(auth_router)

# This is to test if the jwt token verification is working
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    result = session.exec(text("SELECT 1"))
    print("DB Connection test:", result.scalar())

# Note: This is just a test to check if the database connection is working. If it works, it'll print a 1.
