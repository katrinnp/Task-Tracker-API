from fastapi import Depends
from sqlalchemy.orm import Session #Database session type
from typing import Optional, List #For optional types and lists

from app.core.database import get_db
from app.models.task import Task #Task model
from app.schemas.schemas import TaskRead, TaskCreate, TaskUpdate #Pydantic schemas

def get_tasks(completed: Optional[bool] = None, 
              limit: int = 10, #Max tasks per page
               skip: int = 0, #Skip first N tasks
               db: Session = Depends(get_db)): #New database session per request
    query = db.query(Task) #Start with all tasks
    if completed is not None:
        query = query.filter(Task.completed == completed) #Filter tasks by their completed status
    tasks = query.offset(skip).limit(limit).all() #Skip first N tasks, take next M tasks
    return tasks

def create_task(task: TaskCreate, 
                db: Session = Depends(get_db)): #Uses TaskCreate schema to create a new task
    db_task = Task(title=task.title, description = task.description, completed = False)
    db.add(db_task)
    db.commit() #Save changes
    db.refresh(db_task) #Reload instance with generated fields
    return db_task #Returns the created task with status code 201