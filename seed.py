from sqlmodel import Session, select
from database import engine
from models.skill import Skill
from dotenv import load_dotenv
load_dotenv()

skills = [
    {"name": "Python", "category": "Language"},
    {"name": "JavaScript", "category": "Language"},
    {"name": "TypeScript", "category": "Language"},
    {"name": "C++", "category": "Language"},
    {"name": "FastAPI", "category": "Backend"},
    {"name": "Node.js", "category": "Backend"},
    {"name": "PostgreSQL", "category": "Backend"},
    {"name": "React", "category": "Frontend"},
    {"name": "Next.js", "category": "Frontend"},
    {"name": "Figma", "category": "Design"},
    {"name": "UI/UX Design", "category": "Design"},
    {"name": "Machine Learning", "category": "ML"},
    {"name": "TensorFlow", "category": "ML"},
]

with Session(engine) as session:
    for skill in skills:
        existing = session.exec(
            select(Skill).where(Skill.name == skill["name"])
        ).first()
        if not existing:
            session.add(Skill(**skill))
    session.commit()
    print("Skills seeded.")