from fastapi import APIRouter, HTTPException, Query, Depends
from bson import ObjectId
from app.database import client
from app.schemas import ProfileResponse
from app.routers.auth import oauth2_scheme
import math
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"

router = APIRouter()

def clean_profile(profile: dict) -> dict:
    """Clean profile data by removing NaN values and converting ObjectId to string."""
    cleaned = {}
    for key, value in profile.items():
        if isinstance(value, float) and math.isnan(value):
            cleaned[key] = None
        else:
            cleaned[key] = str(value) if isinstance(value, ObjectId) else value
    return cleaned

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        db = client['recommendation_system']
        users = db['users']
        user = await users.find_one({"_id": ObjectId(user_id)})
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except Exception as e:
        logger.error(f"Error in get_current_user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles/me")
async def get_my_profile(current_user = Depends(get_current_user)):
    """Get the current user's profile."""
    try:
        return clean_profile(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profiles/recommended")
async def get_recommended_profiles(current_user: dict = Depends(get_current_user)):
    """Get recommended profiles based on user's liked profiles."""
    try:
        current_user_id = str(current_user.get('_id'))
        logger.info(f"Fetching recommended profiles for user: {current_user_id}")
        
        db = client['recommendation_system']
        users = db['users']
        swipes = db['swipes']
        
        # Get user's liked profiles
        swipes_query = {
            "swiper_id": ObjectId(current_user_id),
            "liked": True
        }
        logger.info(f"Fetching liked profiles with query: {swipes_query}")
        
        liked_profiles = await swipes.find(swipes_query).to_list(length=None)
        num_likes = len(liked_profiles)
        logger.info(f"Found {num_likes} liked profiles")
        
        # Return early if no likes yet
        if num_likes == 0:
            return {
                "status": "success",
                "message": "Please swipe right on a few profiles to get personalized recommendations",
                "data": {
                    "profiles": []
                }
            }
        
        # Get all swiped profiles (both liked and disliked)
        all_swiped = await swipes.find({"swiper_id": ObjectId(current_user_id)}).to_list(length=None)
        all_swiped_ids = [ObjectId(swipe["swiped_id"]) for swipe in all_swiped]
        logger.info(f"Total swiped profiles: {len(all_swiped_ids)}")
        
        # Build base query
        base_query = {
            "_id": {
                "$ne": ObjectId(current_user_id),  # Exclude current user
                "$nin": all_swiped_ids  # Exclude swiped profiles
            }
        }
        
        # Add preferred gender filter
        preferred_gender = current_user.get('preferred_gender')
        if preferred_gender and isinstance(preferred_gender, str):
            preferred_gender = preferred_gender.lower()
            if preferred_gender != 'other':
                base_query["gender"] = {"$regex": f"^{preferred_gender}$", "$options": "i"}
        
        # Get the profiles that the user has liked
        liked_profile_ids = [ObjectId(swipe["swiped_id"]) for swipe in liked_profiles]
        liked_profiles_data = await users.find({"_id": {"$in": liked_profile_ids}}).to_list(length=None)
        
        # Extract characteristics from liked profiles with weights
        feature_weights = {
            "location": 3,        # High weight for location match
            "age": 2.5,          # High weight for age match
            "education_level": 2, # Medium-high weight for education
            "profession": 2,      # Medium-high weight for profession
            "hobbies": 1.5,      # Medium weight for hobbies
            "languages": 1.5,     # Medium weight for languages
            "religion": 1         # Lower weight for religion
        }
        
        # Extract unique values for each feature
        locations = list(set([p.get("location") for p in liked_profiles_data if p.get("location")]))
        education_levels = list(set([p.get("education_level") for p in liked_profiles_data if p.get("education_level")]))
        professions = list(set([p.get("profession") for p in liked_profiles_data if p.get("profession")]))
        religions = list(set([p.get("religion") for p in liked_profiles_data if p.get("religion")]))
        
        # Handle hobbies and languages as arrays or comma-separated strings
        hobbies = []
        languages = []
        for p in liked_profiles_data:
            if p.get("hobbies"):
                if isinstance(p["hobbies"], list):
                    hobbies.extend(p["hobbies"])
                else:
                    hobbies.extend([h.strip() for h in str(p["hobbies"]).split(",")])
            if p.get("languages"):
                if isinstance(p["languages"], list):
                    languages.extend(p["languages"])
                else:
                    languages.extend([l.strip() for l in str(p["languages"]).split(",")])
        
        hobbies = list(set(hobbies))
        languages = list(set(languages))
        
        # Calculate age range based on liked profiles
        ages = [p.get("age") for p in liked_profiles_data if p.get("age")]
        if ages:
            avg_age = sum(ages) / len(ages)
            age_range = 5  # Configurable range
            min_age = max(18, int(avg_age - age_range))
            max_age = int(avg_age + age_range)
        else:
            min_age = max(18, current_user.get('age', 18) - 5)
            max_age = current_user.get('age', 40) + 5
        
        # Use aggregation pipeline for weighted scoring
        pipeline = [
            {"$match": base_query},
            {"$addFields": {
                "hobbiesArray": {
                    "$cond": {
                        "if": {"$isArray": "$hobbies"},
                        "then": "$hobbies",
                        "else": {
                            "$cond": {
                                "if": {"$eq": [{"$type": "$hobbies"}, "string"]},
                                "then": {"$split": ["$hobbies", ","]},
                                "else": []
                            }
                        }
                    }
                },
                "languagesArray": {
                    "$cond": {
                        "if": {"$isArray": "$languages"},
                        "then": "$languages",
                        "else": {
                            "$cond": {
                                "if": {"$eq": [{"$type": "$languages"}, "string"]},
                                "then": {"$split": ["$languages", ","]},
                                "else": []
                            }
                        }
                    }
                }
            }},
            {"$addFields": {
                "score": {
                    "$sum": [
                        # Location score
                        {"$multiply": [
                            {"$cond": [{"$in": ["$location", locations]}, 1, 0]},
                            feature_weights["location"]
                        ]},
                        # Age score
                        {"$multiply": [
                            {"$cond": [
                                {"$and": [
                                    {"$gte": ["$age", min_age]},
                                    {"$lte": ["$age", max_age]}
                                ]},
                                1,
                                0
                            ]},
                            feature_weights["age"]
                        ]},
                        # Education score
                        {"$multiply": [
                            {"$cond": [{"$in": ["$education_level", education_levels]}, 1, 0]},
                            feature_weights["education_level"]
                        ]},
                        # Profession score
                        {"$multiply": [
                            {"$cond": [{"$in": ["$profession", professions]}, 1, 0]},
                            feature_weights["profession"]
                        ]},
                        # Religion score
                        {"$multiply": [
                            {"$cond": [{"$in": ["$religion", religions]}, 1, 0]},
                            feature_weights["religion"]
                        ]},
                        # Hobbies score (partial matches count)
                        {"$multiply": [
                            {"$divide": [
                                {"$size": {"$ifNull": [{"$setIntersection": ["$hobbiesArray", hobbies]}, []]}},
                                {"$max": [1, {"$size": {"$literal": hobbies}}]}
                            ]},
                            feature_weights["hobbies"]
                        ]},
                        # Languages score (partial matches count)
                        {"$multiply": [
                            {"$divide": [
                                {"$size": {"$ifNull": [{"$setIntersection": ["$languagesArray", languages]}, []]}},
                                {"$max": [1, {"$size": {"$literal": languages}}]}
                            ]},
                            feature_weights["languages"]
                        ]}
                    ]
                }
            }},
            {"$sort": {"score": -1}},
            {"$limit": 10}  # Return top 10 matches
        ]
        
        recommended_profiles = await users.aggregate(pipeline).to_list(length=None)
        
        # Clean and return the profiles
        if recommended_profiles:
            cleaned_profiles = [clean_profile(profile) for profile in recommended_profiles]
            logger.info(f"Returning {len(cleaned_profiles)} recommended profiles")
            return {
                "status": "success",
                "message": "Here are your personalized recommendations based on your likes",
                "data": {
                    "profiles": cleaned_profiles
                }
            }
        else:
            logger.info("No recommendations found")
            return {
                "status": "success",
                "message": "No matching recommendations found at this time",
                "data": {
                    "profiles": []
                }
            }
            
    except Exception as e:
        logger.error(f"Error in get_recommended_profiles: {str(e)}")
        logger.exception("Full traceback:")
        return {
            "status": "error",
            "message": "Failed to fetch recommendations",
            "error": str(e)
        }

@router.get("/profiles/next")
async def get_next_profile(current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"Fetching next profile for user: {current_user.get('_id')}")
        logger.info(f"Current user full data: {current_user}")
        
        db = client['recommendation_system']
        users = db['users']
        swipes = db['swipes']
        
        # Get user's preferred gender and normalize it safely
        preferred_gender = current_user.get('preferred_gender')
        if preferred_gender and isinstance(preferred_gender, str):
            preferred_gender = preferred_gender.lower()  # Convert to lowercase for consistency
        logger.info(f"Preferred gender (normalized): {preferred_gender}")
        
        # Get IDs of profiles this user has already swiped on
        try:
            swiped_profiles = await swipes.distinct(
                "swiped_id",
                {"swiper_id": ObjectId(str(current_user["_id"]))}
            )
            logger.info(f"Swiped profiles: {swiped_profiles}")
        except Exception as e:
            logger.error(f"Error getting swiped profiles: {str(e)}")
            swiped_profiles = []
        
        # Build the base query
        query = {
            "_id": {"$ne": ObjectId(str(current_user["_id"]))}  # Exclude current user
        }
        
        # Add gender filter if preferred_gender is specified
        if preferred_gender and preferred_gender != 'other':
            query["gender"] = {"$regex": f"^{preferred_gender}$", "$options": "i"}
        
        # Add swiped profiles filter
        if swiped_profiles:
            query["_id"]["$nin"] = [ObjectId(id) for id in swiped_profiles]
            
        logger.info(f"Final query: {query}")
        
        # First, count total available profiles
        total_profiles = await users.count_documents(query)
        logger.info(f"Total available profiles matching criteria: {total_profiles}")
        
        if total_profiles == 0:
            logger.info("No profiles found matching criteria")
            raise HTTPException(
                status_code=404, 
                detail="No more profiles available matching your preferences"
            )
        
        # Find all matching profiles and get a random one
        profiles = await users.aggregate([
            {"$match": query},
            {"$sample": {"size": 1}}
        ]).to_list(length=1)
        
        logger.info(f"Random profile selected: {profiles[0] if profiles else None}")
        
        if not profiles:
            logger.info("No profiles found after aggregation")
            raise HTTPException(
                status_code=404, 
                detail="No more profiles available matching your preferences"
            )
        
        # Clean and return the profile
        cleaned_profile = clean_profile(profiles[0])
        logger.info(f"Returning cleaned profile: {cleaned_profile}")
        return cleaned_profile
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error in get_next_profile: {str(e)}")
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=str(e))

# This route must be last to avoid conflicts with other /profiles/* routes
@router.get("/profiles/{profile_id}")
async def get_profile(profile_id: str):
    try:
        db = client['recommendation_system']
        users = db['users']
        
        profile = await users.find_one({"_id": ObjectId(profile_id)})
        if profile is None:
            raise HTTPException(status_code=404, detail="Profile not found")
            
        # Clean and return the profile
        return clean_profile(profile)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 