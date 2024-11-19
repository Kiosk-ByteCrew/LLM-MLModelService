from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["kiosk_database"]
collection = db["mycollection"]

# Health check model
class HealthResponse(BaseModel):
    LLMName: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    # Fetch the document from MongoDB
    document = collection.find_one({}, {"_id": 0})  # Exclude the _id field
    if document:
        return HealthResponse(**document)
    return {"error": "Document not found"}

