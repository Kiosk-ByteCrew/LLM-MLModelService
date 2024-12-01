from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from app.databases.mongo import connect_to_mongo, close_mongo_connection
from app.api import health, llm_controller

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()

app = FastAPI(
    title="LLM-MLModel Service",
    description="A service to process data with LLM models.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(llm_controller.router, prefix="/llm", tags=["LLM"])

