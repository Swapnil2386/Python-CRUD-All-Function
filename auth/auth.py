from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
from connections.dependencies import get_db
from jose.exceptions import ExpiredSignatureError


from models import models

# Secret key for JWT encoding/decoding
SECRET_KEY = "thisismysecretkey"  # Use a secure key in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# Token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

FERNET_SECRET = b'tPBmkmMFpgR2ip8JbS0UkZJ5kGSkHaT7hBZYBtbIlCA='  # <-- Generate once and store it securely
fernet = Fernet(FERNET_SECRET)

# Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    jwt_token= jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    encrypted_token = fernet.encrypt(jwt_token.encode()).decode()
    return encrypted_token


# Decode token
def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:

        jwt_token = fernet.decrypt(token.encode()).decode()
        if not jwt_token:
            raise credentials_exception
     
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise credentials_exception
      
        email = payload.get("sub")

        if email is None:
            raise credentials_exception
        # Check if the email exists in the database
        user = db.query(models.User).filter(models.User.email == email).first()
       # user = get_user_by_username(email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or tampered token{str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    