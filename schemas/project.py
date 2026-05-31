from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str
    type: str

class ProjectStatusUpdate(BaseModel):
    status: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int
    status: str
    type:str
    created_at: datetime

    class Config:
        from_attributes= True