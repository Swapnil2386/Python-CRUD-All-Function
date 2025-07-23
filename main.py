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

