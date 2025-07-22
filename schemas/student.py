from typing import Optional
from pydantic import BaseModel

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    classid: int
    classname: Optional[str] = None  # Assuming classname can be optional

    class Config:
        from_attributes = True

# For creating a new student (request body)
class StudentCreate(BaseModel):
    id : Optional [int]  = None  # Assuming id can be optional for creation
    name: str
    email: str
    address: str
    classid: int


# For updating student details (partial update)
class StudentUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    address: str | None = None
    classid: int | None = None

