from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import client
from app.schemas import SwipeCreate
from app.routers.auth import oauth2_scheme
from datetime import datetime
from app.routers.profiles import get_current_user
from pydantic import BaseModel
import logging

router = APIRouter()

class SwipeCreate(BaseModel):
    swiped_id: str
    liked: bool

@router.post("/swipes/")
async def create_swipe(swipe_data: SwipeCreate, current_user: dict = Depends(get_current_user)):
    try:
        db = client['recommendation_system']
        swipes = db['swipes']
        users = db['users']
        
        # Validate that the profile exists
        profile = await users.find_one({"_id": ObjectId(swipe_data.swiped_id)})
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        # Create swipe record
        swipe_record = {
            "swiper_id": current_user["_id"],
            "swiped_id": ObjectId(swipe_data.swiped_id),
            "liked": swipe_data.liked,
            "created_at": datetime.utcnow()
        }
        
        result = await swipes.insert_one(swipe_record)
        
        # Convert ObjectId to string for response
        response = {
            "_id": str(result.inserted_id),
            "swiper_id": str(swipe_record["swiper_id"]),
            "swiped_id": str(swipe_record["swiped_id"]),
            "liked": swipe_record["liked"],
            "created_at": swipe_record["created_at"].isoformat()
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 