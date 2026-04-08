from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    login: str
    url: str

class UserCreate(UserBase):
    id: Optional[int] = None

class UserUpdate(BaseModel):
    login: Optional[str] = None
    url: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True