from sqlalchemy.orm import Session # SQLAlchemy session type for interacting with db
from fastapi import HTTPException, status # FastAPI exceptions and status code

from app.models.user import User # User ORM model
from app.core.security import verify_password, create_access_token # Security utilities for verifying password and creating JWT tokens

def authenticate_user(db: Session,
                      username: str,
                      password: str): # Authenticate user by verifying their username and password
    user = db.query(User).filter(User.username == username).first() # Fetch user by username

    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid username or password")
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid username or password")
    
    return user

def login_user(db: Session,
               username: str,
               password: str): # Authenticate user and generate JWT access token
    user = authenticate_user(db, username, password)

    access_token = create_access_token(
        data = {"sub": user.username}
    ) # Create JWT token with subject set to username

    return {
        "access_token": access_token,
        "token_type": "bearer" # Whoever has this token, has access
    } # Return token response
