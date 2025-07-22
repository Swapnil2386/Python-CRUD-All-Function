
import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from connections.dependencies import get_db


from models.teacher import Teachers
import schemas.teacher as teacher_schema
   


router = APIRouter()

@router.get("/teachers/", response_model=list[teacher_schema.TeacherResponse])
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teachers).all()



@router.post("/teachers/", response_model=teacher_schema.TeacherResponse)
def create_teacher(teacher: teacher_schema.TeacherCreate, db: Session = Depends(get_db)):
    try:
        db_teacher = Teachers(
            TeacherName=teacher.TeacherName,
            TeacherEmail=teacher.TeacherEmail,
            TeacherAddress=teacher.TeacherAddress
        )
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    except Exception as e:
        traceback.print_exc()  # Print full error to console/log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )