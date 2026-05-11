from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Membership(Base):
    __tablename__ = "group_membership"
    id = Column(Integer,
                primary_key = True,
                index = True
    )
    user_id = Column(Integer, # Reference to the user in the membership
                     ForeignKey("users.id"),
                     nullable = False
    )
    group_id = Column(Integer, # Reference to the group in the membership
                      ForeignKey("groups.id"),
                      nullable = False
    )
    role = Column(String, # Role of the user in a specific group
                  default = "Member",
                  nullable = False
    )
    user = relationship("User", # Relationship to the user
                        back_populates="memberships"
    )
    group = relationship("Group", # Relationship to the group
                         back_populates="memberships"
    )
