from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    owner_id: int = Field(foreign_key="user.id")
    status: str = Field(default="open")  # open, full, closed
    type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
