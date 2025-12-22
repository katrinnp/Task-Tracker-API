from fastapi import FastAPI #FastAPI web framework

app = FastAPI(title="Task Tracker API") #Create FastAPI instance

from app.models.task import Task #Task model (database table)
from app.core.database import engine #Database engine, connection with tasks.db
from app.api.v1.tasks import router as tasks_router #Router wih all task endpoints

Task.metadata.create_all(bind=engine) #Create database tables

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"]) #Include tasks router under /tasks path

@app.get("/") 
def read_root(): #Verification that the API is running
    return {"message": "Task Tracker API is running"}

