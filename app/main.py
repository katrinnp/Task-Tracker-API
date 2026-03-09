from fastapi import FastAPI #FastAPI web framework
from fastapi.middleware.cors import CORSMiddleware #Allows requests from frontend
from app.api.v1 import tasks, auth

app = FastAPI(title="Task Tracker API") #Create FastAPI instance

#Frontend addresses that call this API
origins = [
    "http://localhost:5173", #React server
    "http://127.0.0.1:5173"
]

#Enable CORS so React can make requests
app.add_middleware(
    CORSMiddleware, #Built-in FastAPI CORS middleware
    allow_origins=origins, #Allow requests from frontend
    allow_credentials=True, #Allow auth headers to be sent
    allow_methods=["*"], #Allow GET, POST, PUT, PATCH, DELETE
    allow_headers=["*"] #Allow all request headers
)

from app.models.task import Task #Task model (database table)
from app.models.user import User #User model (database table)
from app.core.database import engine #Database engine, connection with tasks.db
from app.api.v1.tasks import router as tasks_router #Router with all task endpoints
from app.api.v1.users import router as users_router #Router with all user endpoints

from app.core.database import Base
Base.metadata.create_all(bind = engine)

app.include_router(tasks_router, prefix = "/tasks", tags = ["Tasks"]) #Include tasks router under /tasks path
app.include_router(users_router, prefix = "/users", tags = ["Users"]) #Include users router under /users path
app.include_router(auth.router, prefix = "/auth", tags = ["Authentication"]) #Include authentication router

@app.get("/") 
def read_root(): #Verification that the API is running
    return {"message": "Task Tracker API is running"}

