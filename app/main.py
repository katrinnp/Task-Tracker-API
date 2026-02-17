from fastapi import FastAPI #FastAPI web framework
from app.api.v1 import tasks, auth

app = FastAPI(title="Task Tracker API") #Create FastAPI instance

from app.models.task import Task #Task model (database table)
from app.models.user import User #User model (database table)
from app.core.database import engine #Database engine, connection with tasks.db
from app.api.v1.tasks import router as tasks_router #Router wih all task endpoints
from app.api.v1.users import router as users_router #Router with all user endpoints

from app.core.database import Base
Base.metadata.create_all(bind = engine)

app.include_router(tasks_router, prefix = "/tasks", tags = ["Tasks"]) #Include tasks router under /tasks path
app.include_router(users_router, prefix = "/users", tags = ["Users"]) #Include users router under /users path
app.include_router(auth.router, prefix = "/auth", tags = ["Authentication"]) # Include authentication router

@app.get("/") 
def read_root(): #Verification that the API is running
    return {"message": "Task Tracker API is running"}

