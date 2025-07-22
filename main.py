from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from connections.database import Base,  SessionLocal , engine
import models.models as models
from sqlalchemy.orm import Session

from typing import Annotated
from fastapi import Depends
from routers import user, teacher,student



Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router,prefix="/api", tags=["users"])
app.include_router(teacher.router, prefix="/api", tags=["teachers"])
app.include_router(student.router, prefix="/api", tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#DBSession = Annotated[Session, Depends(get_db)]


# @app.get("/users/", response_model=list[schema.UserResponse])
# def get_users(db: DBSession):
#     return db.query(models.User).all()

# @app.post("/users/", response_model=schema.UserResponse)
# def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = models.User(**user.model_dump())  # Unpack Pydantic data
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# @app.put("/users/{user_id}", response_model=schema.UserResponse)
# def update_user(user_id: int, user_update: schema.UserUpdate, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     update_data = user_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_user, key, value)

#     db.commit()
#     db.refresh(db_user)
#     return db_user


# @app.get("/users/")
# def get_users():
#     users = db.query(models.User).all()
#     return users

# @app.post("/users/", response_model=User, status_code=201)
# def create_user(user: User):
#     db_user = models.User(id = user.id,name=user.name, email=user.email, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# @app.post("/users/")
# def create_user(user: models.User,response_model=User,status_code=201):
#     db_user = models.User(id = user.id,name=user.name, email=user.email, password=user.password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# @app.get("/")
# def read_root():
#     return {"message": "Hello, World!"} 

# @app.get("/students/{student_id}")
# def read_student(student_id: int):
#     return {"student_id": student_id, "name": "John Doe", "age": 20}

# @app.post("/students/")
# def create_student(student: Student):
#     return {"message": "Student created", "student": student}