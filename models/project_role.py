from sqlmodel import SQLModel, Field
from typing import Optional

class ProjectRole(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    name: str
    total_spots: int
    filled_spots: int = Field(default=0)

