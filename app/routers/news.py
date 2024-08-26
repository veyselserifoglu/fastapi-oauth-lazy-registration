from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.services.dependencies import create_session
from app.core.database import get_db
from app.core.templates import templates
from app.models.sessions import Session as session_model
from app.services.dependencies import get_current_user


news_router = APIRouter(
    prefix="/news", 
    tags=["news"]
)


@news_router.get("/news", response_class=HTMLResponse)
async def show_news(
    request: Request, 
    response: Response,
    db: Session = Depends(get_db),
    user_data: dict = Depends(get_current_user)
): 
    # fetch user's data.
    username = user_data["username"]
    user_session_token = user_data["user_session"].session_token

    # build the response 
    response =  templates.TemplateResponse("news.html", {"request": request, "username": username})

    # set cookies.
    response.set_cookie(
        key="session_token",
        value=user_session_token,
        httponly=True,
        secure=False,  # Set to True in production
        samesite="Lax"
    )

    return response

@news_router.get("/comment", response_class=HTMLResponse)
async def add_comment(
    request: Request, 
    db: Session = Depends(get_db),
    user_data: dict = Depends(get_current_user)
):
    
    # fetch user's data.
    username = user_data["username"]
    user_session_token = user_data["user_session"]

    if username == 'Anonymous':
        return templates.TemplateResponse("signup.html", {"request": request}) 
    
    return templates.TemplateResponse("news.html", {"request": request, "username": username})

