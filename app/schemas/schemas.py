from pydantic import BaseModel #Base class for data validation
from typing import Optional, List #For optional types in Python 3.9
from datetime import datetime #For timestamp fields
from pydantic import EmailStr # Provides automatic email format validation


#Defines how a task is returned to the client
class TaskRead(BaseModel): #Reading a task
    id: int #Database id of the task
    title: str 
    description: Optional[str] = None
    completed: bool
    created_at: datetime #Creation timestamp
    updated_at: Optional[datetime] = None #Last update timestamp
    user_id: int #id for user who owns this task
    class Config:
        from_attributes = True #Allows Pydantic to read from SQLAlchemy ORM objects


class TaskCreate(BaseModel): #Creating a new task
    title: str
    description: Optional[str] = None #Optional description

class TaskReplace(BaseModel): #Replacing an existing task
    title: str
    description: Optional[str] = None
    completed: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class UserCreate(BaseModel):
    username: str # Username of the new user
    email: EmailStr # Used for authentication
    password: str # Pass received from user

class UserRead(BaseModel):
    id: int
    username: str
    role: str # User role

    class Config:
        from_attributes = True # Allows reading from SQLAlchemy models

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class MembershipCreate(BaseModel):
    user_id: int
    role: str = "Member"

class MembershipRead(BaseModel):
    user_id: int
    group_id: int
    role: str

    class Config:
        from_attributes = True

class GroupBase(BaseModel): # Base schema for Group
    name: str # Name of the group

class GroupCreate(GroupBase): # Used when creating a group
    pass

class GroupRead(GroupBase): # Used for returning group data
    id: int 
    memberships: List[MembershipRead] = []
    
    class Config:
        from_attributes = True # Allows reading from ORM models