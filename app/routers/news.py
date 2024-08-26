from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.services.dependencies import create_session, get_current_user
from app.core.database import get_db
from app.core.templates import templates


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

@news_router.get("/comment", response_class=RedirectResponse)
async def add_comment():
    return RedirectResponse(url="/auth/signup")