from pydantic import BaseModel

class ProjectRoleCreate(BaseModel):
    project_id: int
    name: str
    total_spots: int = 1

class ProjectRoleUpdate(BaseModel):
    name: str | None = None
    total_spots: int | None = None
    filled_spots: int | None = None

class ProjectRoleResponse(BaseModel):
    id: int
    project_id: int
    name: str
    total_spots: int
    filled_spots: int

    class Config:
        from_attributes = True