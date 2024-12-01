from app.databases.mongo import get_database
from app.helpers.exceptions import SessionInactiveError
from app.models.llm_conversation import LlmConversationRequest, LlmConversationResponse
from app.models.llm_request import LLMRequest
from fastapi.encoders import jsonable_encoder

llm_metadata_collection = "kiosk_llm_session_metadata"

async def save_metadata(data: LLMRequest) -> dict:
    db = get_database()
    result = await db[llm_metadata_collection].insert_one(jsonable_encoder(data))
    return {"data": "metadata saved", "inserted_id": str(result.inserted_id)}

async def get_entries() -> list:
    db = get_database()
    entries = await db[llm_metadata_collection].find().to_list(length=None)
    for entry in entries:
        entry['id'] = str(entry['_id'])
    return entries


async def validate_conversation_request(request: LlmConversationRequest):
    db = get_database()
    if not request.user_id:
        raise ValueError("User ID is required.")
    if not request.session_id:
        raise ValueError("Session ID is required.")
    if not request.messages:
        raise ValueError("messages is required.")
    if not request.timezone:
        raise ValueError("Timezone is required.")

    query = {
        'session_id': request.session_id
    }
    result = await db[llm_metadata_collection].find_one(query)
    if result:
        if result.get('status') != 'active':
            raise SessionInactiveError(request.session_id)
    else:
        raise SessionInactiveError(request.session_id)


async def make_conversation(request: LlmConversationRequest) -> LlmConversationResponse:
    await validate_conversation_request(request)
    # TODO: integration of selected OpenAI API or any open source model.

    return LlmConversationResponse(
        user_id="uid1",
        session_id="sesid1",
        message_id="uid1_sesid1_2",
        prompt_response="We have a Veggie Delight that will go perfectly with your preferences.",
        timezone="America/New_York"
    )

