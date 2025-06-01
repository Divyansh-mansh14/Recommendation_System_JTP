from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Enum, JSON
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Profile Information
    name = Column(String)
    age = Column(Integer)
    gender = Column(Enum(Gender))
    preferred_gender = Column(Enum(Gender))  
    religion = Column(String)
    location = Column(String)
    education_level = Column(String)
    profession = Column(String)
    
    # Lifestyle & Personality
    smoking = Column(Boolean)
    drinking = Column(Boolean)
    diet = Column(String)
    hobbies = Column(JSON)  
    languages = Column(JSON)  
    
    swipes_given = relationship("Swipe", foreign_keys="Swipe.swiper_id", back_populates="swiper")
    swipes_received = relationship("Swipe", foreign_keys="Swipe.swiped_id", back_populates="swiped")

class Swipe(Base):
    __tablename__ = "swipes"

    id = Column(Integer, primary_key=True, index=True)
    swiper_id = Column(Integer, ForeignKey("users.id"))
    swiped_id = Column(Integer, ForeignKey("users.id"))
    liked = Column(Boolean)  
    timestamp = Column(Float)  
    
    swiper = relationship("User", foreign_keys=[swiper_id], back_populates="swipes_given")
    swiped = relationship("User", foreign_keys=[swiped_id], back_populates="swipes_received") 