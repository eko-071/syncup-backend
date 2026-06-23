from pydantic import BaseModel

class ProjectRoleCreate(BaseModel):
    project_id: int
    role_name: str
    spots: int = 1

class ProjectRoleUpdate(BaseModel):
    role_name: str | None = None
    spots: int | None = None
    filled: int | None = None

class ProjectRoleResponse(BaseModel):
    id: int
    project_id: int
    role_name: str
    spots: int
    filled: int

    class Config:
        from_attributes = True