from passlib.context import CryptContext # Used for password hashing
from jose import jwt, JWTError # Used for JWT token creation and catch decoding errors
from datetime import datetime, timedelta # Used for token expiration

from app.core.config import settings # Import project settings from .env

# Configuration algorithm for hashing
pwd_context = CryptContext( # Defines the hashing algorithm (bcrypt)
    schemes = ["bcrypt"], # Use bcrypt hashing algorithm
    deprecated = "auto"
    )

def hash_password(password: str) -> str: # Hashes a password using bcrypt
    return pwd_context.hash(password) # This is what we store in db

def verify_password(password: str, hashed_password: str) -> bool: # Compares a password with a hashed password
    return pwd_context.verify(password, hashed_password) # Returns true if match

def create_access_token(data: dict) -> str: # Creates JWT token with expiration time
    to_encode = data.copy() # Copy payload
    expire = datetime.utcnow() + timedelta(minutes = settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm = settings.algorithm) # Create and sign the JWT token with secret key
    return encoded_jwt

def decode_access_token(token: str) -> dict: # Decodes JWT token and returns payload
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError: # Raises an exception if the token is invalid or expired
        return None

