from pydantic import BaseModel

class TeacherResponse(BaseModel):
    Id: int
    TeacherName: str
    TeacherEmail: str
    TeacherAddress: str

    class Config:
        from_attributes = True
        # For creating a new teacher (request body)
class TeacherCreate(BaseModel):
    TeacherName: str
    TeacherEmail: str
    TeacherAddress: str

# For updating teacher details (partial update)
class TeacherUpdate(BaseModel):
    TeacherName: str | None = None
    TeacherEmail: str | None = None
    TeacherAddress: str | None = None