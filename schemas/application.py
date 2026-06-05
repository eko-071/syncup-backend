from pydantic import BaseModel
from datetime import datetime

class ApplicationCreate(BaseModel):
    project_role_id: int

class ApplicationStatusUpdate(BaseModel):
    status: str

class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    project_role_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
