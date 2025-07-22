from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connections.dependencies import get_db
from auth.auth import create_access_token
from utility.password_utility import hash_password, verify_password

from models import models
from schemas import schema

#router = APIRouter(prefix="/api/users", tags=["users"])
router = APIRouter()

@router.get("/users/", response_model=list[schema.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/users/", response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())  # Unpack Pydantic data
    db_user.hashpassword = hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/users/{user_id}", response_model=schema.UserResponse)
def update_user(user_id: int, user_update: schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/users/login", response_model=schema.Token)
def login(user_login: schema.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_login.username).first()
    # Get the hashed password from the database user record
    if not user:
        raise HTTPException(status_code=400, detail="user Invalid credentials")
    _hashpassword_user = hash_password(user.password)

    verified = verify_password(user_login.password, _hashpassword_user)

    if not user or not _hashpassword_user:
        raise HTTPException(status_code=400, detail="hash Invalid credentials")
    if not verified:
        raise HTTPException(status_code=400, detail="verifyed Invalid credentials")
    
    # If the user is found and the password is correct, create a token
    access_token = create_access_token(data={"sub": user.email})
    return schema.Token(access_token=access_token, token_type="bearer")



@router.get("/users/{user_id}", response_model=schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user