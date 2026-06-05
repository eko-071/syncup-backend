from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.application import Application
from models.project_role import ProjectRole
from models.user import User
from security.jwt import get_current_user
from schemas.application import ApplicationCreate
from schemas.application import ApplicationResponse

router= APIRouter(prefix="/applications", tags=["applications"])

#create application
@router.post("/", response_model=ApplicationResponse)
def create_application(
    application: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    session: Session= Depends(get_session)
):
    role=session.exec(
        select(ProjectRole).where(
            ProjectRole.id==application.project_role_id
        )
    ).first()
    if not role:
        raise HTTPException(
            status_code=404,
            detail="Project role not found"
        )
    existing=session.exec(
        select(Application)
        .where(Application.user_id==current_user.id)
        .where(
            Application.project_role_id==
            application.project_role_id
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already applied"
        )
    db_application=Application(
        user_id=current_user.id,
        project_role_id=application.project_role_id
    )
    session.add(db_application)
    session.commit()
    session.refresh(db_application)
    return db_application

#get my applications
@router.get("/me", response_model=list[ApplicationResponse])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    session: Session= Depends(get_session)
):
    applications=session.exec(
        select(Application)
        .where(Application.user_id==current_user.id)
    ).all()
    return applications

#get application by id
@router.get("/{id}", response_model=ApplicationResponse)
def get_application(
    id:int,
    session: Session = Depends(get_session)
):
    application=session.exec(
        select(Application)
        .where(Application.id==id)
    ).first()
    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    return application

@router.delete("/{id}")
def remove_application(
    id: int,
    current_user: User= Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_application=session.exec(
        select(Application)
        .where(Application.id==id)
    ).first()
    if not db_application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )
    if db_application.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )
    session.delete(db_application)
    session.commit()
    return {"message": "Application withdrawn"}
