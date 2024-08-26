from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.services.dependencies import create_session
from app.core.database import get_db
from app.core.templates import templates
from app.models.sessions import Session as session_model


news_router = APIRouter(
    prefix="/news", 
    tags=["news"]
)


@news_router.get("/news", response_class=HTMLResponse)
async def show_news(request: Request, response: Response, db: Session = Depends(get_db)):

    # TODO: 1. check if we need to have a unique identifier for every anonymous user.
    # TODO: 2. add a middleware
     
    # Check if the user already has a session cookie
    session_token = request.cookies.get("session_token") 

    response = templates.TemplateResponse("news.html", {"request": request})
    
    # Create a new session if one doesn't exist
    if not session_token:
        db_session = create_session(db)

        session_token = db_session.session_token

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,     # Prevents JavaScript access to the cookie
            secure=False,      # Ensures the cookie is only sent over HTTPS
            samesite="Lax",    # Controls cross-site request behavior
        )

    return response

@news_router.get("/comment", response_class=HTMLResponse)
async def add_comment(request: Request, db: Session = Depends(get_db)):
    # Retrieve the session token from the cookies
    session_token = request.cookies.get("session_token")
    if session_token is None:
        return templates.TemplateResponse("news.html", {"request": request}) 
    
    # Fetch the session object from the database using the session token
    session_data = db.query(session_model).filter_by(session_token=session_token).first()
    
    # if session data is expired or does not exist, redirect to the landing page.
    if not session_data:
        return templates.TemplateResponse("landing_page.html", {"request": request})
    
    # if session doesn't have a user, redirect to the signup page.
    if not session_data.user_id:
        return templates.TemplateResponse("signup.html", {"request": request}) 

    return templates.TemplateResponse("news.html", {"request": request}) 

