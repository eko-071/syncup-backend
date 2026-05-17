from sqlmodel import SQLModel, Field

class UserSkill(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    skill_id: int = Field(foreign_key="skill.id", primary_key=True)
    proficiency: str  # stuff like "beginner", "intermediate", "advanced"