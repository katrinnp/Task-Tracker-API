from fastapi import Depends, status, HTTPException #FastAPI dependency, status code, errors
from sqlalchemy.orm import Session #Database session type
from typing import Optional, List #For optional types and lists

from app.models.task import Task #Task model
from app.schemas.schemas import TaskRead, TaskCreate, TaskUpdate #Pydantic schemas
from app.core.database import get_db #Database session dependency (new database session per request)
from fastapi import APIRouter #Routing

router = APIRouter() #Used to group and organise task-related endpoints in FastAPI

@router.get("/", response_model=List[TaskRead])
def get_tasks(completed: Optional[bool] = None, db: Session = Depends(get_db)): #Return all tasks
    query = db.query(Task)
    if completed is not None:
        query = query.filter(Task.completed == completed) #Filter tasks by their completed status
    tasks = query.all()
    return tasks

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)): #Uses TaskCreate schema to create a new task
    db_task = Task(title=task.title, description=task.description, completed=False)
    db.add(db_task)
    db.commit() #Save changes
    db.refresh(db_task) #Reload instance with generated fields
    return db_task #Returns the created task with status code 201

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)): #Retrieve a task by its id
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found") #Raises 404 if the task does not exist
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)): #Updates an existing task
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    #Partial update
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT) #Returns 204 NO CONTENT
def delete_task(task_id: int, db: Session = Depends(get_db)): #Deletes a task by its id
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task) #Mark task for deletion
    db.commit() #Execute deletion
    return None #Response 204 must not contain a body