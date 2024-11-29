from fastapi import FastAPI
from app.api.v1.endpoints import health

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])