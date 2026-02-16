from fastapi import HTTPException # Tools for routing and dependency
from sqlalchemy.orm import Session # Session for db

from app.core.security import hash_password # Import password hashing
from app.models.user import User # User table in db
from app.schemas.schemas import UserCreate, UserUpdate # Pydantic schemas for validation

def create_user(user: UserCreate,
                db: Session): # Creates new db session per request, closes automatically in the end
    db_user = User(username = user.username,
                   email = user.email,
                   hashed_password = hash_password(user.password)) # Creates a new user instance

    db.add(db_user) # Adds the user to db session
    db.commit() # Save changes
    db.refresh(db_user) # Refresh to get generated fields

    return db_user


def get_users(db: Session): # Retrieve all users from db
    return db.query(User).all()


def get_user(db: Session, #Retrieve a single user by id
             user_id: int):
    user = db.query(User).filter(User.id == user_id).first() # Search user by id

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found") # If user does not exist, return 404 error
    
    return user

def update_user(db: Session,
                user_id: int,
                user_update: UserUpdate): # Partially update user
    user = get_user(db, user_id)

    if user_update.username is not None:
        user.username = user_update.username

    if user_update.email is not None:
        user.email = user_update.email

    if user_update.password is not None:
        user.hashed_password = hash_password(user_update.password) # Hash new password

    db.commit()
    db.refresh(user)
    
    return user

def delete_user(db: Session, user_id: int): # Delete user by id
    user = get_user(db, user_id)

    db.delete(user)
    db.commit()

    return None

    