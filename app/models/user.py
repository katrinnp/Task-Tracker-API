from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship #Used to define ORM relationships between models
from app.core.database import Base #For model to become a database table
from app.models.group import user_group # Import association table

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, 
                primary_key = True, #Unique identifier
                index = True) #DB index for faster lookups
    username = Column(String, 
                      unique = True, #No duplicates allowed
                      index = True,
                      nullable = False) #Required field
    # This will be used for login
    email = Column(String,
                   unique = True,
                   index = True,
                   nullable = True)
    # Hashed password, this stores the encrypted version of the password
    hashed_password = Column(String,
                      nullable = True)
    # Role for the user
    role = Column(
        String,
        default="USER"
    )
    # One to many: a user can have many tasks
    tasks = relationship(
        "Task", #Related model
        back_populates = "owner") #Connects this relationship to the "owner", creating a two-way link
    # Many to many
    groups = relationship(
        "Group",
        secondary=user_group,
        back_populates="users"
    )
    # One to many: groups where this user is the admin
    admin_groups = relationship(
        "Group",
        back_populates="admin" #Connects this relationship to the "admin", creating a two-way link
    )