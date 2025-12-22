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

    class Config:
        from_attributes = True #Allows Pydantic to read from SQLAlchemy ORM objects


class TaskCreate(BaseModel): #Creating a new task
    title: str
    description: Optional[str] = None #Optional description

class TaskUpdate(BaseModel): #Updating an existing task
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None