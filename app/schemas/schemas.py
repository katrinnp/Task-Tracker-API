from pydantic import BaseModel #Base class for data validation
from typing import Optional #For optional types in Python 3.9
from datetime import datetime #For timestamp fields

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
    user_id: int # required to link task to a user

class TaskReplace(BaseModel): #Replacing an existing task
    title: str
    description: Optional[str] = None
    completed: bool

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class UserCreate(BaseModel):
    username: str #Username of the new user

class UserRead(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True #Allows reading from SQLAlchemy models

