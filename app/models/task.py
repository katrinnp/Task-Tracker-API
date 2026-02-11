from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    description = Column(String, nullable = True)
    completed = Column(Boolean, default = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    updated_at = Column(DateTime(timezone = True), onupdate = func.now())
    user_id = Column(Integer, 
                     ForeignKey("users.id"), #Links each task to a specific user
                     nullable = False)
    owner = relationship("User", back_populates = "tasks") #ORM relationship back to the User model

    