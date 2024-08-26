from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    session_token = Column(String, unique=True, index=True, nullable=False)

    # Nullable for anonymous sessions
    # one to many relationship ==> one user can have multiple sessions. 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  

    # back_populate: can access the user object from the session object
    user = relationship("User", back_populates="sessions")