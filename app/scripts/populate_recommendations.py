from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import asyncio

# Sample recommendations data
sample_recommendations = [
    {
        "title": "Python Programming",
        "description": "Master Python programming with hands-on projects",
        "rating": 4.8,
        "category": "Programming",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Web Development",
        "description": "Learn full-stack web development",
        "rating": 4.9,
        "category": "Web Development",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Data Science",
        "description": "Introduction to data science and machine learning",
        "rating": 4.7,
        "category": "Data Science",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Mobile App Development",
        "description": "Build mobile apps for iOS and Android",
        "rating": 4.6,
        "category": "Mobile Development",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Cloud Computing",
        "description": "Learn AWS, Azure, and Google Cloud",
        "rating": 4.5,
        "category": "Cloud",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def populate_recommendations():
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        db = client['recommendation_system']
        recommendations = db['recommendations']
        
        # Clear existing recommendations
        await recommendations.delete_many({})
        print("Cleared existing recommendations")
        
        # Insert sample recommendations
        result = await recommendations.insert_many(sample_recommendations)
        print(f"Successfully inserted {len(result.inserted_ids)} recommendations")
        
        # Create indexes
        await recommendations.create_index("title")
        await recommendations.create_index("category")
        print("Created indexes")
        
        # Verify the data
        count = await recommendations.count_documents({})
        print(f"Total recommendations in database: {count}")
        
        # Display some sample data
        async for doc in recommendations.find().limit(2):
            print(f"Sample recommendation: {doc}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(populate_recommendations()) 