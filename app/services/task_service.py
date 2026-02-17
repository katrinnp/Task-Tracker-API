from fastapi import status, HTTPException  # FastAPI status code, errors
from sqlalchemy.orm import Session  # Database session type
from typing import Optional  # For optional types

from app.models.task import Task  # Task model
from app.schemas.schemas import TaskCreate, TaskReplace, TaskUpdate  # Pydantic schemas


def get_tasks(db: Session,  # Database session passed from router
            user_id: int,
            completed: Optional[bool] = None,
            limit: int = 10,  # Max tasks per page
            skip: int = 0):  # Skip first N tasks
    query = db.query(Task).filter(Task.user_id == user_id)  # Start with all tasks

    if completed is not None:
        query = query.filter(Task.completed == completed)  # Filter tasks by their completed status

    tasks = query.offset(skip).limit(limit).all()  # Skip first N tasks, take next M tasks
    return tasks


def create_task(db: Session,  # Database session passed from router
                task: TaskCreate, # Uses TaskCreate schema to create a new task
                user_id: int):
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=False, 
        user_id = user_id
    )

    db.add(db_task)
    db.commit()  # Save changes
    db.refresh(db_task)  # Reload instance with generated fields

    return db_task  # Returns the created task


def get_task_by_id(db: Session,  # Database session passed from router
                    task_id: int,
                    user_id: int):  # Retrieve a task by its id
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )  # Raises 404 if the task does not exist

    return task


def update_task(db: Session,  # Database session passed from router
                task_id: int,
                task_update: TaskReplace,
                user_id: int): # Updates an existing task
    task = get_task_by_id(db, task_id, user_id)  # Reuse existing function

    # Replace whole
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed

    db.commit()
    db.refresh(task)

    return task

def patch_task(db: Session, # Database session passed from router
               task_id: int,
               task_update: TaskUpdate,
               user_id: int): # Updates an existing task
    task = get_task_by_id(db, task_id, user_id) # Reuse existing function

    # Partial update
    if task_update.title is not None:
        task.title = task_update.title
    
    if task_update.description is not None:
        task.description = task_update.description
    
    if task_update.completed is not None:
        task.completed = task_update.completed

    db.commit()
    db.refresh(task)

    return task

def delete_task(db: Session,  # Database session passed from router
                task_id: int,
                user_id: int):  # Deletes a task by its id
    task = get_task_by_id(db, task_id, user_id)  # Reuse existing function

    db.delete(task)  # Mark task for deletion
    db.commit()  # Execute deletion
