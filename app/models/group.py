from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base 

# Association table for many to many relationship between users and groups
user_group = Table(
    "user_group",
    Base.metadata, # Stores all database schema
    Column("user_id", Integer, ForeignKey("users.id")), # Users table
    Column("group_id", Integer, ForeignKey("groups.id")) # Groups table
)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable = False)
    # Foreign key to the user who is the admin of this group
    admin_id = Column(Integer, ForeignKey("users.id"))
    # Relationship to the admin user
    admin = relationship("User", back_populates="admin_groups")
    # Many to many relationship with users
    users = relationship(
        "User",
        secondary=user_group,
        back_populates="groups"
    )