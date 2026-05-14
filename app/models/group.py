from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base 

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    # One group can have many memberships
    memberships = relationship("Membership",
                               back_populates = "group",
                               cascade = "all, delete-orphan"
    )

