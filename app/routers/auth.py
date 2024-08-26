from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.dependencies import create_session, get_current_user
from app.core.database import get_db

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/anonymous/")
async def anonymous_session(db: Session = Depends(get_db)):
    session = create_session(db)
    return {"session_token": session.session_token}

@auth_router.post("/signup/")
async def signup(email: str, password: str, db: Session = Depends(get_db)):
    # Logic to create a new user and return the session token
    pass
