import jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

# Secret key for JWT encoding/decoding
SECRET_KEY = "thisismysecretkey"  # Use a secure key in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize OAuth2PasswordBearer for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Utility function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify the JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

# Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
