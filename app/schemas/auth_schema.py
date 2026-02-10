from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    age_group: str
    avatar: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse

class SignupRequest(BaseModel):
    name: str
    email: str
    age_group: str
    password: str

class SignupResponse(BaseModel):
    user: UserResponse
    access_token: str
