import os
import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from database import get_session
from models.user import User
from jose import jwt
from datetime import datetime, timezone, timedelta
from security.google_auth import get_google_login_url, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_TOKEN_URL, GOOGLE_USERINFO_URL

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_jwt_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.get("/google")
def google_login():
    return RedirectResponse(get_google_login_url())

@router.get("/google/callback")
async def google_callback(code: str, session: Session = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(GOOGLE_TOKEN_URL, data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        })
        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token from Google")

        user_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_info = user_response.json()

    # Check if user exists
    existing_user = session.exec(
        select(User).where(User.google_id == user_info["id"])
    ).first()

    if existing_user:
        jwt_token = create_jwt_token(existing_user.id)
    else:
        new_user = User(
            name=user_info["name"],
            email=user_info["email"],
            google_id=user_info["id"],
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        jwt_token = create_jwt_token(new_user.id)

    return RedirectResponse(url=f"http://localhost:3000/auth/callback?token={jwt_token}")