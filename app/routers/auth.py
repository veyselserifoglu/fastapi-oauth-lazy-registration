from fastapi import APIRouter, Depends, Request
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
async def signup(request: Request, db: Session = Depends(get_db), 
                 username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Logic to create a new user and associate with the session
    new_user = user_model(
        username=username, 
        email=email, 
        hashed_password=password  # hash_password(password)
    )
    db.add(new_user)
    db.commit()
    
    # Associate the session with the new user
    session_token = request.cookies.get("session_token")
    if session_token is None:
        # Redirect to the news page or another appropriate page
        return RedirectResponse(url="/news/news", status_code=303) 
    
    # fetch the current user's session and link it with the new user record.
    session_data = db.query(session_model).filter_by(session_token=session_token).first()
    if session_data:
        session_data.user_id = new_user.id
        db.commit()

    # Redirect to the news page or another appropriate page
    return RedirectResponse(url="/news/news", status_code=303)