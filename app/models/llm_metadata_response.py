from bson import ObjectId
from pydantic import BaseModel, Field

class LlmMetadata(BaseModel):
    id: str = Field(..., description="Unique identifier for the entry.")
    user_id: str = Field(..., description="Unique identifier for the user.")
    user_name: str = Field(..., description="Name of the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")
    status: str = Field(..., description="Status of the session.")

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "60d5ec49f8d2e30d8c8b4567",
                "user_id": "12345",
                "user_name": "bob",
                "session_id": "session1234",
                "status": "Active"
            }
        }

class LlmMetadataEntriesResponse(BaseModel):
    entries: list[LlmMetadata]

    class Config:
        json_encoders = {ObjectId: str}
