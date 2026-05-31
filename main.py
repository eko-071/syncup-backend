from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, text, Session
from database import engine
from models.user import User
from models.skill import Skill
from models.user_skill import UserSkill
from models.project import Project
from models.project_role import ProjectRole
from models.application import Application
from routers.auth import router as auth_router
from routers.users import router as users_router
from routers.skills import router as skills_router
from routers.projects import router as projects_router
from security.jwt import get_current_user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(skills_router)
app.include_router(projects_router)


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    result = session.exec(text("SELECT 1"))
    print("DB Connection test:", result.scalar())

# Note: This is just a test to check if the database connection is working. If it works, it'll print a 1.
