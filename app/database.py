import motor.motor_asyncio
import pymongo
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "recommendation_system")

# Create a synchronous client for testing connection
sync_client = pymongo.MongoClient(MONGODB_URL)

# Test the connection
def test_connection():
    try:
        sync_client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return True
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return False

# Create async client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

# Collections
users = db.users
swipes = db.swipes
recommendations = db.recommendations

# Helper function to convert MongoDB ObjectId to string
def serialize_object_id(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

# Function to initialize the database with indexes
async def init_db():
    """Initialize database with required collections and indexes."""
    try:
        # Drop existing indexes
        await users.drop_indexes()
        await swipes.drop_indexes()
        await recommendations.drop_indexes()
        
        # Create indexes for users collection
        await users.create_index("email", unique=True)
        await users.create_index("name")
        await users.create_index("location")
        await users.create_index("gender")
        await users.create_index("preferred_gender")
        
        # Create indexes for swipes collection
        await swipes.create_index([("swiper_id", 1), ("swiped_id", 1)], unique=True)
        await swipes.create_index("created_at")
        
        # Create indexes for recommendations collection
        await recommendations.create_index([("user_id", 1), ("recommended_id", 1)], unique=True)
        await recommendations.create_index("created_at")
        
        logger.info("Database initialization complete")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e

async def close_db():
    client.close()
    sync_client.close() 