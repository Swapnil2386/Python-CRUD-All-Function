from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    password: str

    class Config:
        from_attributes = True


        # For creating a new user (request body)
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# For updating user details (partial update)
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
