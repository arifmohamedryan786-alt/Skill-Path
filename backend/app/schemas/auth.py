from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    full_name: str
    email: Optional[str] = None
    career_goal: Optional[str] = None
    goal_status: Optional[str] = None
    is_guest: Optional[bool] = False

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "learner"  # "learner" or "admin"

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

