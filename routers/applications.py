from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.application import Application
from models.project_role import ProjectRole
from models.user import User
from security.jwt import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

# Apply for a project role
@router.post("/")
def create_application(
    project_role_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    role = session.exec(
        select(ProjectRole)
        .where(ProjectRole.id == project_role_id)
    ).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Project role not found"
        )
    existing = session.exec(
        select(Application)
        .where(Application.user_id == current_user.id)
        .where(Application.project_role_id == project_role_id)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already applied"
        )
    application = Application(
        user_id=current_user.id,
        project_role_id=project_role_id
    )
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

# Get my applications
@router.get("/me")
def get_my_applications(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.exec(
        select(Application)
        .where(Application.user_id == current_user.id)
    ).all()

# Get application by ID
@router.get("/{application_id}")
def get_application(
    application_id: int,
    session: Session = Depends(get_session)
):
    application = session.exec(
        select(Application)
        .where(Application.id == application_id)
    ).first()
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    return application

# Withdraw my application
@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    application = session.exec(
        select(Application)
        .where(Application.id == application_id)
    ).first()
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    if application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    session.delete(application)
    session.commit()
    return {"message": "Application withdrawn"}
