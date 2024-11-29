from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db.mongo import collection
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

router = APIRouter()

class HealthResponse(BaseModel):
    LLMName: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        print(MONGO_URI)
        print(DATABASE_NAME)
        print(COLLECTION_NAME)
        # Fetch a document from MongoDB
        document = collection.find_one({}, {"_id": 0})
        if document:
            return HealthResponse(**document)
        raise HTTPException(status_code=404, detail="Document not found")
    except ServerSelectionTimeoutError as e:
        raise HTTPException(status_code=500, detail=f"MongoDB connection error: {str(e)}")