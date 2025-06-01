from pydantic import BaseModel, EmailStr, conlist, validator
from typing import List, Optional
from enum import Enum
from datetime import datetime

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    
    @classmethod
    def _missing_(cls, value):
        """Handle case-insensitive matching"""
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.value == value:
                    return member
        return None

class UserBase(BaseModel):
    email: EmailStr
    name: str
    age: int
    gender: Gender
    preferred_gender: Gender
    religion: Optional[str] = None
    location: Optional[str] = None
    education_level: Optional[str] = None
    profession: Optional[str] = None
    smoking: bool = False
    drinking: bool = False
    diet: Optional[str] = None
    hobbies: List[str] = []
    languages: List[str] = []
    
    @validator('gender', 'preferred_gender', pre=True)
    def normalize_gender(cls, v):
        if isinstance(v, str):
            v = v.lower()
            if v not in [g.value for g in Gender]:
                raise ValueError(f'Invalid gender value: {v}')
        return v

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class SwipeCreate(BaseModel):
    swiped_id: int
    liked: bool

class Swipe(SwipeCreate):
    id: int
    swiper_id: int
    timestamp: float

    class Config:
        from_attributes = True

class ProfileResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: Gender
    religion: Optional[str] = None
    location: Optional[str] = None
    education_level: Optional[str] = None
    profession: Optional[str] = None
    smoking: bool = False
    drinking: bool = False
    diet: Optional[str] = None
    hobbies: List[str] = []
    languages: List[str] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None 