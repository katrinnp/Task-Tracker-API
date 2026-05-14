from fastapi import APIRouter, Depends, HTTPException, status # Tools for routing and dependency
from sqlalchemy.orm import Session # Session for db
from typing import List

from app.core.database import get_db # Creates a new db session per request
from app.models.user import User # User table in db
from app.schemas.schemas import UserCreate, UserRead, UserUpdate, LoginRequest # Pydantic schemas for validation
from app.services import user_service
from app.core.permissions import is_admin, can_manage_user
from app.core.dependencies import get_current_user

router = APIRouter() # Used to group and organise user-related endpoints in FastAPI

# Public endpoint for user registration
@router.post("/", response_model = UserRead, status_code = status.HTTP_201_CREATED)
def create_user(user: UserCreate,
                db: Session = Depends(get_db)): # Creates new user
    return user_service.create_user(db, user)

# Only admin can see all users
@router.get("/", response_model = List[UserRead])
def get_users(db: Session = Depends(get_db), 
              current_user: User = Depends(get_current_user)): # Retrieve all users from db
    if not is_admin(current_user):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "Admin privileges required")
    return user_service.get_users(db)

# A user can view themselves and users they manage
@router.get("/{user_id}", response_model = UserRead)
def get_user(user_id: int, #Retrieve a single user by id
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    target_user = user_service.get_user(db, user_id)
    if current_user.id != target_user.id and not can_manage_user(db, current_user, target_user):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "No permission")
    return target_user

# User can update themselves and users they manage
@router.patch("/{user_id}", response_model = UserRead)
def update_user(user_id: int, 
                user_update: UserUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)): # Partially update user data
    target_user = user_service.get_user(db, user_id)
    if current_user.id != target_user.id and not can_manage_user(db, current_user, target_user):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = "No permission")
    return user_service.update_user(db, user_id, user_update)

@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)): # Delete a user by id
    if not is_admin(current_user):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin privileges required"
        )
    return user_service.delete_user(db, user_id)

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return user_service.login_user(db, data)