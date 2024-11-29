from fastapi import APIRouter
from pymongo.collection import Collection
from pydantic import BaseModel
#from app.db.mongo import collection

# Router for health check
router = APIRouter()

# Health check response model
class HealthResponse(BaseModel):
    LLMName: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    document = {"LLMName": "Application is up"}
    return HealthResponse(**document)