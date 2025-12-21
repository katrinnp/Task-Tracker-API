from fastapi import FastAPI, Depends, status, HTTPException #FastAPI web framework + dependency


app = FastAPI(title="Task Tracker API") #Create FastAPI instance

from app.models.task import Task #Task model
from app.core.database import engine #Database engine, connection with tasks.db
from app.core.database import get_db #Database session dependency (new database session per request)
from sqlalchemy.orm import Session #Session type (database connection)
from pydantic import BaseModel #Data validation
from typing import Optional, List #For types in Python 3.9
from datetime import datetime

class TaskRead(BaseModel): #Reading a task
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True #Read from SQLAlchemy objects
class TaskCreate(BaseModel): #Creating a new task
    title: str
    description: Optional[str] = None #Optional description

class TaskUpdate(BaseModel): #Updating a task
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

Task.metadata.create_all(bind=engine) #Create tasks table in database

@app.get("/") 
def read_root():
    return {"message": "Task Tracker API is running"} #JSON response in browser

@app.get("/tasks", response_model=List[TaskRead]) #Returns all tasks as list
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all() #Fetch all tasks
    return tasks #FastAPI will serialize the list of tasks to JSON

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskRead) #Creates new task (returns 201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(title=task.title, description=task.description, completed=False)
    db.add(db_task) 
    db.commit() 
    db.refresh(db_task) 
    return db_task #Return as JSON

@app.get("/tasks/{task_id}", response_model=TaskRead) #Get a task by id
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first() #First line where id mathes task_id
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found") #Returns standard 404 JSON response
    return task

@app.put("/tasks/{task_id}", response_model=TaskRead) #Updates an existing task
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT) #Delete task by id (returns 204 for empty body/ 404 if task does not exist)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return None