from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class LlmMessageContent(BaseModel):
    id: str = Field(..., description="The id of the message")
    content: str = Field(..., description="The content of the message")
    content_type: str = Field(..., description="The content type of the message")
    created_time: datetime = Field(..., description="The time the message was created")

    class Config:
        schema_extra = {
            "example": {
                "id": "uid1_sesId1_2",  # userId_sesseionId_messagecounter
                "content": "Hi, suggest a burger.",
                "content_type": "text",
                "created_time": 1733005478.182
            }
        }


class LlmConversationRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user.")
    session_id: str = Field(..., description="Unique identifier for the session.")
    messages: List[LlmMessageContent] = Field(..., description="Messages sent by the user.")
    parent_message_id: str = Field(..., description="Unique identifier for the parent message.")
    timezone: str = Field(..., description="Timezone of the conversation.")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "uid1",
                "session_id": "sesid1",
                "messages": [
                    {
                        "id": "uid1_sesId1_2",  # userId_sesseionId_messagecounter
                        "content": "Hi, suggest a burger.",
                        "content_type": "text",
                        "created_time": 1733005478.182
                    }
                ],
                "parent_message_id": "uid1_sesId1_1",
                "timezone": "America/New_York"
            }
        }


class LlmConversationResponse(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the session.")
    prompt_response: str = Field(..., description="Prompt response of the conversation.")
    action: dict = Field(..., description="action")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "sesid1",
                "prompt_response": "We have a Veggie Delight that will go perfectly with your preferences.",
                "action": {"finalize_order": 1}
            }
        }


class LlmStaticConversationRequest(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the session.")
    message: str = Field(..., description="Messages sent by the user.")
    start_conversation: bool = Field(..., description="Is this message start of conversation.")

    class Config:
        schema_extra = {
            "example": {
                "session_id": "sesid1",
                "message": "Hi, suggest a burger.",
                "start_conversation": True
            }
        }