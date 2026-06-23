from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.project_role import ProjectRole
from models.project import Project
from models.user import User
from security.jwt import get_current_user
from schemas.project_role import ProjectRoleCreate, ProjectRoleUpdate, ProjectRoleResponse

router = APIRouter(prefix="/project-roles", tags=["project-roles"])

# Create a role for a project
@router.post("/", response_model=ProjectRoleResponse)
def create_role(
    role: ProjectRoleCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    project = session.exec(select(Project).where(Project.id == role.project_id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_role = ProjectRole(**role.model_dump())
    session.add(db_role)
    session.commit()
    session.refresh(db_role)
    return db_role

# Get all roles for a project
@router.get("/project/{project_id}", response_model=list[ProjectRoleResponse])
def get_roles_for_project(project_id: int, session: Session = Depends(get_session)):
    roles = session.exec(
        select(ProjectRole).where(ProjectRole.project_id == project_id)
    ).all()
    return roles

# Get a single role
@router.get("/{id}", response_model=ProjectRoleResponse)
def get_role(id: int, session: Session = Depends(get_session)):
    role = session.exec(select(ProjectRole).where(ProjectRole.id == id)).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# Update a role
@router.patch("/{id}", response_model=ProjectRoleResponse)
def update_role(
    id: int,
    update: ProjectRoleUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    role = session.exec(select(ProjectRole).where(ProjectRole.id == id)).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    project = session.exec(select(Project).where(Project.id == role.project_id)).first()
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(role, key, value)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role

# Delete a role
@router.delete("/{id}")
def delete_role(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    role = session.exec(select(ProjectRole).where(ProjectRole.id == id)).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    project = session.exec(select(Project).where(Project.id == role.project_id)).first()
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    session.delete(role)
    session.commit()
    return {"message": "Role deleted"}