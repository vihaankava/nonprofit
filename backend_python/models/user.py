from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import uuid4


class UserProfile(BaseModel):
    first_name: str
    last_name: str
    location: Optional[str] = None
    interests: Optional[List[str]] = None
    experience: Optional[str] = None


class User(BaseModel):
    user_id: str
    email: EmailStr
    password_hash: str
    profile: UserProfile
    created_at: datetime
    last_login_at: datetime


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str
    profile: UserProfile


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    user_id: str
    email: EmailStr
    profile: UserProfile
    created_at: datetime
    last_login_at: datetime


class AuthResponse(BaseModel):
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    user: UserResponse
    token: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    timestamp: datetime