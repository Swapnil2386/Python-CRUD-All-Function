import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import text
from sqlalchemy.orm import Session
from connections.dependencies import get_db
from auth.auth import get_current_user

from models.student import Students
import schemas.student as student_schema

router = APIRouter()

@router.get("/students/", response_model=list[student_schema.StudentResponse])
def get_students(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    result = db.execute(text("SELECT * FROM getAllStudents()")) 
    strudents = result.fetchall()
    return [
        {
           "id": student.id,
            "name": student.name,
            "email": student.email,
            "address": student.address,
            "classid": student.classid,
            "classname": student.classname
        }
        for student in strudents
    ]
@router.post("/students/", response_model=student_schema.StudentResponse)
def create_student(student: student_schema.StudentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        db.execute(
            text("CALL InsertStudent(:name, :email, :address, :classid)"),
            {
                "name": student.name,
                "email": student.email,
                "address": student.address,
                "classid": student.classid
            }
        )
        db.commit()
        result = db.execute(
            text('SELECT * FROM "Students" WHERE email = :email'),
            {"email": student.email}
        ).fetchone()
        if result:
            return {
                "id": result.id,
                "name": result.name,
                "email": result.email,
                "address": result.address,
                "classid": result.classid  # or result.classid based on DB naming
            }
        else:
            raise HTTPException(status_code=404, detail="Student not found after insert")

        #  result = db.execute(
        #     text('SELECT * FROM "Students" WHERE email = :email'),
        #     {"email": student.email}
        # ).fetchone()
        # if not result:
        #     raise HTTPException(status_code=404, detail="Student not found")
      
        # sql = text("CALL InsertStudent(:name, :email, :address, :classid)")
        # db.execute(sql, {
        #     "name": student.name,
        #     "email": student.email,
        #     "address": student.address,
        #     "classid": student.classid
        # })
        # db.commit()
         
       
    except Exception as e:
        traceback.print_exc()  # Print full error to console/log
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )   
    
