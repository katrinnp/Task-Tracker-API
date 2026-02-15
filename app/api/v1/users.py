from fastapi import APIRouter, Depends, HTTPException, status # Tools for routing and dependency
from sqlalchemy.orm import Session # Session for db
from typing import List

from app.core.database import get_db # Creates a new db session per request
from app.models.user import User # User table in db
from app.schemas.schemas import UserCreate, UserRead # Pydantic schemas for validation

router = APIRouter() # Used to group and organise user-related endpoints in FastAPI

@router.post("/", response_model = UserRead, status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate,
                db: Session = Depends(get_db)): # Creates new db session per request, closes automatically in the end
    db_user = User(username = user.username,
                   email = user.email,
                   hashed_password = user.password) # Creates a new user instance

    db.add(db_user) # Adds the user to db session
    db.commit() # Save changes
    db.refresh(db_user) # Refresh to get generated fields

    return db_user

@router.get("/", response_model = List[UserRead])
def get_users(db: Session = Depends(get_db)): # Retrieve all users from db
    return db.query(User).all()

@router.get("/{user_id}", response_model = UserRead)
def get_user(user_id: int, #Retrieve a single user by id
             db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first() # Search user by id

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found") # If user does not exist, return 404 error
    
    return user

