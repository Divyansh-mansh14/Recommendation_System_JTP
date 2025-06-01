from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class RecommendationBase(BaseModel):
    title: str
    description: str
    rating: float
    category: str

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationUpdate(RecommendationBase):
    pass

class Recommendation(RecommendationBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int
    gender: str
    preferred_gender: str
    location: str
    religion: Optional[str] = None
    education_level: Optional[str] = None
    profession: Optional[str] = None
    smoker: Optional[str] = None
    drinker: Optional[str] = None
    diet: Optional[str] = None
    hobbies: Optional[List[str]] = []
    languages: Optional[List[str]] = []
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 