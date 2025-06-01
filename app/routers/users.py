from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
from app.schemas import User, UserCreate, UserUpdate, UserResponse
from app.routers.auth import get_password_hash, oauth2_scheme
from app.database import client
import logging

router = APIRouter()

@router.get("/users")
async def get_users(
    skip: int = 0,
    limit: int = 10,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None,
    gender: Optional[str] = None,
    preferred_gender: Optional[str] = None,
    location: Optional[str] = None
):
    try:
        # Build query
        query = {}
        if age_min is not None or age_max is not None:
            query["age"] = {}
            if age_min is not None:
                query["age"]["$gte"] = age_min
            if age_max is not None:
                query["age"]["$lte"] = age_max
        
        if gender:
            query["gender"] = gender
        
        if preferred_gender:
            query["preferred_gender"] = preferred_gender
            
        if location:
            query["location"] = {"$regex": location, "$options": "i"}

        # Get database reference
        db = client['recommendation_system']
        users = db['users']

        # Execute query with projection to include all fields
        cursor = users.find(query, {
            "_id": 1,
            "name": 1,
            "age": 1,
            "gender": 1,
            "location": 1,
            "preferences": 1,
            "preferred_gender": 1,
            "profile_image": 1,
            "created_at": 1,
            "updated_at": 1
        }).skip(skip).limit(limit)
        
        results = []
        async for user in cursor:
            user["_id"] = str(user["_id"])
            results.append(user)
            
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    try:
        db = client['recommendation_system']
        users = db['users']
        
        user = await users.find_one({"_id": ObjectId(user_id)})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        user["_id"] = str(user["_id"])
        return user
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/match/{user_id}")
async def get_matches(
    user_id: str,
    limit: int = 10,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None
):
    try:
        db = client['recommendation_system']
        users = db['users']
        
        # Get user preferences
        user = await users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Build match query
        match_query = {
            "_id": {"$ne": ObjectId(user_id)},  # Exclude the user themselves
            "gender": user.get("preferred_gender") if user.get("preferred_gender") != "Other" else {"$exists": True},
        }
        
        # Add age filter if specified
        if min_age or max_age:
            match_query["age"] = {}
            if min_age:
                match_query["age"]["$gte"] = min_age
            if max_age:
                match_query["age"]["$lte"] = max_age
                
        # Find matches with projection to include profile image
        matches = []
        async for match in users.find(
            match_query,
            {
                "_id": 1,
                "name": 1,
                "age": 1,
                "gender": 1,
                "location": 1,
                "preferences": 1,
                "profile_image": 1
            }
        ).limit(limit):
            match["_id"] = str(match["_id"])
            matches.append(match)
            
        return matches
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users", response_model=User)
async def create_user(user: UserCreate):
    try:
        db = client['recommendation_system']
        users = db['users']
        
        # Check if user already exists
        existing_user = await users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user document
        user_dict = user.model_dump()
        
        # Validate required fields
        required_fields = ['name', 'email', 'age', 'gender', 'preferred_gender', 'location']
        missing_fields = [field for field in required_fields if not user_dict.get(field)]
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )
        
        # Validate age
        if not isinstance(user_dict['age'], int) or user_dict['age'] < 18:
            raise HTTPException(
                status_code=400,
                detail="Age must be a number and at least 18 years old"
            )
        
        # Hash password
        user_dict["password"] = get_password_hash(user_dict["password"])
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        # Insert user
        result = await users.insert_one(user_dict)
        
        # Get created user
        created_user = await users.find_one({"_id": result.inserted_id})
        if not created_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
            
        created_user["_id"] = str(created_user["_id"])
        return created_user
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error creating user: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}") 