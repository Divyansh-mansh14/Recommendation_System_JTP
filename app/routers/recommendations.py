from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas import Recommendation, RecommendationCreate, RecommendationUpdate
from app.database import client
from bson import ObjectId
from datetime import datetime
from app.routers.auth import oauth2_scheme
import logging

router = APIRouter()

@router.post("/recommendations", response_model=Recommendation)
async def create_recommendation(recommendation: RecommendationCreate):
    try:
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        recommendation_dict = recommendation.model_dump()
        recommendation_dict["created_at"] = datetime.utcnow()
        recommendation_dict["updated_at"] = datetime.utcnow()
        
        result = await recommendations.insert_one(recommendation_dict)
        created_recommendation = await recommendations.find_one({"_id": result.inserted_id})
        return {**created_recommendation, "_id": str(created_recommendation["_id"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations", response_model=List[Recommendation])
async def get_recommendations(skip: int = 0, limit: int = 10, search: str = None, category: str = None):
    try:
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        query = {}
        
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        
        if category:
            query["category"] = category

        cursor = recommendations.find(query).skip(skip).limit(limit)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{recommendation_id}", response_model=Recommendation)
async def get_recommendation(recommendation_id: str):
    try:
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        result = await recommendations.find_one({"_id": ObjectId(recommendation_id)})
        if result is None:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        result["_id"] = str(result["_id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Invalid recommendation ID")

@router.put("/recommendations/{recommendation_id}", response_model=Recommendation)
async def update_recommendation(recommendation_id: str, recommendation: RecommendationUpdate):
    try:
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        recommendation_dict = recommendation.model_dump(exclude_unset=True)
        recommendation_dict["updated_at"] = datetime.utcnow()
        
        result = await recommendations.find_one_and_update(
            {"_id": ObjectId(recommendation_id)},
            {"$set": recommendation_dict},
            return_document=True
        )
        
        if result is None:
            raise HTTPException(status_code=404, detail="Recommendation not found")
            
        result["_id"] = str(result["_id"])
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail="Invalid recommendation ID")

@router.delete("/recommendations/{recommendation_id}")
async def delete_recommendation(recommendation_id: str):
    try:
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        result = await recommendations.delete_one({"_id": ObjectId(recommendation_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        return {"message": "Recommendation deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Invalid recommendation ID") 