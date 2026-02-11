from fastapi import Depends, status #FastAPI dependency, status code, errors
from sqlalchemy.orm import Session #Database session type
from typing import Optional, List #For optional types and lists

from app.schemas.schemas import TaskRead, TaskCreate, TaskReplace, TaskUpdate #Pydantic schemas
from app.models.user import User
from app.models.task import Task #Task model
from app.schemas.schemas import TaskRead, TaskCreate, TaskUpdate #Pydantic schemas
from app.core.database import get_db #Database session dependency (new database session per request)
from fastapi import APIRouter #Routing

from app.services import task_service

router = APIRouter() #Used to group and organise task-related endpoints in FastAPI

@router.get("/", response_model = List[TaskRead])
def get_tasks(completed: Optional[bool] = None, limit: int = 10, #Max tasks per page
>>>>>>> eb14db8 (Update task endpoints and schemas)
               skip: int = 0, #Skip first N tasks
               user_id: Optional[int] = None,
               db: Session = Depends(get_db)): #New database session per request
    return task_service.get_tasks(db, completed, limit, skip)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = TaskRead)
def create_task(task: TaskCreate, 
                db: Session = Depends(get_db)): #Uses TaskCreate schema to create a new task
    return task_service.create_task(db, task)

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, 
             db: Session = Depends(get_db)): #Retrieve a task by its id
    return task_service.get_task_by_id(db, task_id)

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, 
                task_update: TaskReplace, 
                db: Session = Depends(get_db)): #Updates an existing task
    return task_service.update_task(db, task_id, task_update)

@router.patch("/{task_id}", response_model = TaskRead)
def patch_task(task_id: int,
               task_update: TaskUpdate,
               db: Session = Depends(get_db)):
    return task_service.patch_task(db, task_id, task_update)

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT) #Returns 204 NO CONTENT
def delete_task(task_id: int, 
                db: Session = Depends(get_db)): #Deletes a task by its id
    task_service.delete_task(db, task_id)
=======
    query = db.query(Task) #Start with all tasks
    if completed is not None:
        query = query.filter(Task.completed == completed) #Filter tasks by their completed status
    if user_id is not None:
        query = query.filter(Task.user_id == user_id) #Filter tasks by user
    tasks = query.offset(skip).limit(limit).all() #Skip first N tasks, take next M tasks
    return tasks

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)): #Uses TaskCreate schema to create a new task

    user = db.query(User).filter(User.id == task.user_id).first()
    if user is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    db_task = Task(title = task.title, description = task.description, completed = False, user_id = task.user_id)
    db.add(db_task)
    db.commit() #Save changes
    db.refresh(db_task) #Reload instance with generated fields
    return db_task #Returns the created task with status code 201

@router.get("/{task_id}", response_model = TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)): #Retrieve a task by its id
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found") #Raises 404 if the task does not exist
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)): #Updates an existing task
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found")
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

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT) #Returns 204 NO CONTENT
def delete_task(task_id: int, db: Session = Depends(get_db)): #Deletes a task by its id
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Task not found")
    db.delete(task) #Mark task for deletion
    db.commit() #Execute deletion
    return None #Response 204 must not contain a body
>>>>>>> eb14db8 (Update task endpoints and schemas)
