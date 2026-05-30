from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Application(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    project_role_id: int = Field(foreign_key="projectrole.id")
    status: str = Field(default="pending")  # pending, accepted, rejected
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))