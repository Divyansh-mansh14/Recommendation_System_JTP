from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.recommendations import router as recommendations_router
from app.routers.profiles import router as profiles_router
from app.routers.swipes import router as swipes_router
from app.database import init_db, test_connection
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With"
    ],
    expose_headers=["*"],
    max_age=3600
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(users_router, prefix="/api", tags=["users"])
app.include_router(recommendations_router, prefix="/api", tags=["recommendations"])
app.include_router(profiles_router, prefix="/api", tags=["profiles"])
app.include_router(swipes_router, prefix="/api", tags=["swipes"])

@app.on_event("startup")
async def startup_event():
    try:
        # Test MongoDB connection
        if not test_connection():
            logger.error("Failed to connect to MongoDB. Please check your connection settings.")
            return

        # Initialize database
        await init_db()
        logger.info("Application startup complete")
    except Exception as e:
        logger.error(f"Error during startup: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Recommendation System API"} 