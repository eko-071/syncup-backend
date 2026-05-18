from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import jwt, JWTError
from database import get_session
from models.user import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user