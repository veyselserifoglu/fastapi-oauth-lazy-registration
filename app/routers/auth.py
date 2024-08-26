from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse

from app.services.dependencies import create_session, get_current_user
from app.core.database import get_db

from app.models.users import User as user_model
from app.models.sessions import Session as session_model

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request, 
    db: Session = Depends(get_db),              
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...),

    user_data: dict = Depends(get_current_user)
):  
    
    username = user_data["username"]
    user_session = user_data["user_session"]

    # Logic to create a new user and associate with the session
    new_user = user_model(
        username=username, 
        email=email, 
        hashed_password=password  # hash_password(password)
    )
    db.add(new_user)
    db.commit()

    if user_session:
        user_session.user_id = new_user.id
        db.commit()

    # Redirect to the news page or another appropriate page
    return RedirectResponse(url="/news/news", status_code=303)

@auth_router.get("/logout")
async def logout(
    request: Request, 
    response: Response, 
    db: Session = Depends(get_db),
    user_data: dict = Depends(get_current_user)
):
    
    user_session = user_data["user_session"]
        
    # Delete the session from the database only if the user is anonymous
    if not user_session.user_id:
        db.delete(user_session)
        db.commit()

    # Delete the session cookie by setting it to an empty value
    response.set_cookie(
        key="session_token",
        value=""
    )

    return RedirectResponse(url="/", status_code=303)