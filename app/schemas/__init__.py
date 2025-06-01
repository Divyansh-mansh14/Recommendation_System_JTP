"""
Schema package for the dating profile recommender system.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: str
    location: str
    preferred_gender: str
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    location: Optional[str] = None
    preferred_gender: Optional[str] = None
    profile_image: Optional[str] = None

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    location: str
    profile_image: Optional[str] = None

class ProfileResponse(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    location: str
    profile_image: Optional[str] = None

class SwipeCreate(BaseModel):
    swiped_id: str
    liked: bool

class RecommendationBase(BaseModel):
    title: str
    description: str
    rating: float
    category: str

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    category: Optional[str] = None

class Recommendation(RecommendationBase):
    id: str = Field(alias="_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 