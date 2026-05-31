from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.project import Project
from models.user import User
from security.jwt import get_current_user
from schemas.project import ProjectCreate
from schemas.project import ProjectStatusUpdate
from schemas.project import ProjectResponse
router= APIRouter(prefix="/projects", tags=["projects"])

#create project
@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: Session= Depends(get_session)
):
    db_project= Project(**project.model_dump(), owner_id=current_user.id)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    status: str | None= None,
    type: str |None=None,
    session: Session = Depends(get_session)
):
    query = select(Project)
    if status:
        query = query.where(Project.status==status)
    if type:
        query= query.where(Project.type==type)
    projects= session.exec(query).all()
    return projects

#get single project by id
@router.get("/{id}", response_model=ProjectResponse)
def get_id(
    id:int,
    session: Session = Depends(get_session)
):
    project= session.exec(select(Project).where(Project.id==id)).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{id}", response_model=ProjectResponse)
def update_project_status(
    id: int,
    project: ProjectStatusUpdate,
    current_user: User= Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_project=session.exec(select(Project).where(Project.id==id)).first()

    if not db_project:
        raise HTTPException(status_code= 404, detail="Project Not Found")
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_project.status=project.status
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project


@router.delete("/{id}")
def remove_project(
    id: int,
    current_user: User= Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_project=session.exec(select(Project).where(Project.id==id)).first()

    if not db_project:
        raise HTTPException(status_code= 404, detail="Project Not Found")
    if db_project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    session.delete(db_project)
    session.commit()
    return {"message": "Project deleted"}