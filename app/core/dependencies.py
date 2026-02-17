from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # Used to read Bearer token from Authorization header
from jose import JWTError, jwt # JWT decoding
from sqlalchemy.orm import Session # SQLAlchemy database session

from app.core.config import settings # SECRET_KEY, algorithm
from app.core.database import get_db # DB session dependency
from app.models.user import User # User ORM model

# Reads "Authorization: Bearer <token>"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), # Extract token from request
                     db: Session = Depends(get_db)): # Get db session
    # Raised when token is invalid
    exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                              detail = "Could not validate",
                              headers = {"WWW-Authenticate": "Bearer"})
    
    try:
        # Decode token and read username from "sub"
        payload = jwt.decode(token, settings.secret_key, algorithms = [settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    # Find user in db
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise exception
    
    return user
    
    