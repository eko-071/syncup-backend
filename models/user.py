from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    google_id: str = Field(unique=True)
    bio: Optional[str] = None
    experience_level: Optional[str] = None
    availability: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))