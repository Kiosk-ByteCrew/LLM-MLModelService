from fastapi import APIRouter

router = APIRouter()

@router.get("", summary="Health Check")
async def health_check():
    return {"status": "LLM-MLModel Service is up and running."}