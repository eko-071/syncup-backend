from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.user import User
from models.user_skill import UserSkill
from models.skill import Skill
from security.jwt import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

# Get my profile
@router.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Update my profile
@router.patch("/me")
def update_my_profile(
    updates: dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    allowed_fields = {"name", "bio", "experience_level", "availability"}
    for key, value in updates.items():
        if key in allowed_fields:
            setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

# Get any user by ID
@router.get("/{user_id}")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# List all users, optionally filter by skill
@router.get("/")
def list_users(
    skill: str | None = None,
    session: Session = Depends(get_session)
):
    if skill:
        users = session.exec(
            select(User)
            .join(UserSkill)
            .join(Skill)
            .where(Skill.name == skill)
        ).all()
    else:
        users = session.exec(select(User)).all()
    return users

# Add a skill to my profile
@router.post("/me/skills/{skill_id}")
def add_skill(
    skill_id: int,
    proficiency: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    skill = session.exec(select(Skill).where(Skill.id == skill_id)).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    existing = session.exec(
        select(UserSkill)
        .where(UserSkill.user_id == current_user.id)
        .where(UserSkill.skill_id == skill_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Skill already added")

    user_skill = UserSkill(user_id=current_user.id, skill_id=skill_id, proficiency=proficiency)
    session.add(user_skill)
    session.commit()
    return {"message": "Skill added"}

# Remove a skill from my profile
@router.delete("/me/skills/{skill_id}")
def remove_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_skill = session.exec(
        select(UserSkill)
        .where(UserSkill.user_id == current_user.id)
        .where(UserSkill.skill_id == skill_id)
    ).first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="Skill not found on profile")
    session.delete(user_skill)
    session.commit()
    return {"message": "Skill removed"}