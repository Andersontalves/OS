from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=3, max_length=100)
    role: str = Field(..., pattern="^(admin|monitoramento|execucao|campo)$")
    nome: Optional[str] = Field(None, max_length=150)
    telegram_id: Optional[int] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    username: Optional[str] = None
    role: Optional[str] = Field(None, pattern="^(admin|monitoramento|execucao|campo)$")
    nome: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Login Schemas
class LoginRequest(BaseModel):
    """Schema for login request"""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
