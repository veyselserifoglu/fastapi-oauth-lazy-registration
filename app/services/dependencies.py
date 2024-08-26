import uuid
from fastapi import Depends, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sessions import Session as session_model
from app.models.users import User as user_model

def create_session(db: Session, user_id: int = None):
    session_token = str(uuid.uuid4())

    db_session = session_model(session_token=session_token, user_id=user_id)
    db.add(db_session)

    db.commit()
    db.refresh(db_session)
    
    return db_session

def get_session_token_from_cookies(request: Request):
    return request.cookies.get("session_token")


def validate_session_token(session_token: str, db: Session) -> session_model:
    if not session_token:
        return None

    session_data = db.query(session_model).filter_by(session_token=session_token).first()
    return session_data
    
def get_user_from_session(session_data: session_model, db: Session) -> str:
    if session_data and session_data.user_id:
        user = db.query(user_model).filter_by(id=session_data.user_id).first()
        if user:
            return user.username
    return "Anonymous"

def get_current_user(request: Request, db: Session = Depends(get_db), response: Response = None) -> str:
    # Step 1: Extract session token from cookies
    session_token = get_session_token_from_cookies(request)
    
    # Step 2: Validate session token against the database
    session_data = validate_session_token(session_token, db)
    
    # Step 3: If session is valid, get the user
    if session_data:
        username = get_user_from_session(session_data, db)
    
    # Step 4: If session is invalid, invalidate and create a new session
    if not session_token or not session_data:
        session_data = create_session(db)
        username = "Anonymous"
    
    # Default to anonymous if no valid session or user is found
    return {"username": username, "user_session": session_data}