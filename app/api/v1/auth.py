from fastapi import APIRouter, Depends, status # Router and FastAPI dependency
from fastapi.security import OAuth2PasswordRequestForm # Form data for username/password login

from sqlalchemy.orm import Session

from app.schemas.schemas import Token
from app.core.database import get_db
from app.services import auth_service # Auth business logic

router = APIRouter()

@router.post("/login", response_model = Token, status_code = status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), # Authomatically reads form fields: username and password
          db: Session = Depends(get_db)): # Login endpoint, returns JWT access token
    return auth_service.login_user(
        db = db,
        username = form_data.username,
        password = form_data.password
    )
    


