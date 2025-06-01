# This file makes the routers directory a Python package 
from .auth import router as auth_router
from .users import router as users_router
from .recommendations import router as recommendations_router
from .profiles import router as profiles_router
from .swipes import router as swipes_router 