from passlib.context import CryptContext # Used for password hashing
from jose import jwt # Used for JWT token creation
from datetime import datetime, timedelta # Used for token expiration

# Configuration settings for JWT authentication
SECRET_KEY = "secret-key" # Used to sign JWT tokens
ALGORITHM = "HS256" # Used for JWT encoding
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token expiration time

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
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM) # Create and sign the JWT token with secret key
    return encoded_jwt



