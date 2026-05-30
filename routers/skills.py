from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.skill import Skill

router = APIRouter(prefix="/skills", tags=["skills"])

# List all skills
@router.get("/")
def list_skills(session: Session = Depends(get_session)):
    return session.exec(select(Skill)).all()

# Get skills by category
@router.get("/category/{category}")
def get_skills_by_category(category: str, session: Session = Depends(get_session)):
    skills = session.exec(select(Skill).where(Skill.category == category)).all()
    if not skills:
        raise HTTPException(status_code=404, detail="No skills found for this category")
    return skills