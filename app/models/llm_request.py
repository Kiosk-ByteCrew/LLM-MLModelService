from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user.")
    user_name: str = Field(..., description="Name of the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")
    status: str = Field(..., description="Status of the session.")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345",
                "user_name": "John Doe",
                "session_id": "session1234",
                "status": "Active"
            }
        }
