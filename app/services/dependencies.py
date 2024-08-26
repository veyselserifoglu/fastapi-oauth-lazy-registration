import uuid
from fastapi import Depends
from sqlalchemy.orm import Session
from app.models.sessions import Session as DBSession
from app.core.database import get_db

def create_session(db: Session, user_id: int = None):
    session_token = str(uuid.uuid4())

    db_session = DBSession(session_token=session_token, user_id=user_id)
    db.add(db_session)

    db.commit()
    db.refresh(db_session)
    
    return db_session

def get_current_user(db: Session = Depends(get_db)):
    # Logic to retrieve the current user based on the session token, if any
    pass
