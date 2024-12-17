from fastapi import APIRouter

from app.models.llm_conversation import LlmConversationRequest, LlmConversationResponse, LlmStaticConversationRequest
from app.models.llm_metadata_response import LlmMetadataEntriesResponse
from app.models.llm_request import LLMRequest
from app.services.llm_service import save_metadata, get_entries, make_conversation

router = APIRouter()


@router.post("/metadata/save", summary="store metadata for each session")
async def llm_metadata_save(request: LLMRequest):
    return await save_metadata(request)


@router.get("/metadata/fetch", summary="fetch call", response_model=LlmMetadataEntriesResponse)
async def llm_metadata_save():
    entries = await get_entries()
    return {"entries": entries}


@router.post("/conversation", summary="conversation with model", response_model=LlmConversationResponse)
async def llm_conversation(request: LlmStaticConversationRequest):
    result = await make_conversation(request)
    return result
