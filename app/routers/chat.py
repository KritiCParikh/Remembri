from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import asyncio

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.llm_service import LLMService
from app.services import memory_service

load_dotenv()

router = APIRouter(prefix="/chat", tags=["chat"])

# -------- Database Dependency --------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- LLM Dependency --------
def get_llm_service():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    api_key = "hello"
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    return LLMService(api_key)

# -------- Pydantic Models --------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# -------- Helper Function: Format Memory --------
def format_memories(memories):
    if not memories:
        return "No stored memories."
    return "\n".join([f"{m.key}: {m.content}" for m in memories])

# -------- POST Endpoint --------
@router.post("")
async def chat_post(request: ChatRequest, 
                    llm_service: LLMService = Depends(get_llm_service),
                    db: Session = Depends(get_db)):
    """
    Process a chat message via POST and return a streaming response with memory context
    """
    # 1. Fetch memories from DB
    memories = memory_service.get_memories(db)
    memory_context = format_memories(memories)

    # 2. Prepare combined prompt
    full_prompt = f"""Here is what you remember:
{memory_context}

User: {request.message}
Assistant:"""

    # 3. Stream response
    return StreamingResponse(
        llm_service.stream_response(full_prompt),
        media_type="text/event-stream"
    )

# -------- GET Endpoint --------
@router.get("")
async def chat_get(request: Request, 
                   llm_service: LLMService = Depends(get_llm_service),
                   db: Session = Depends(get_db)):
    """
    Process a chat message via GET and return a streaming response with memory context
    """
    message = request.query_params.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # 1. Fetch memories from DB
    memories = memory_service.get_memories(db)
    memory_context = format_memories(memories)

    # 2. Prepare combined prompt
    full_prompt = f"""Here is what you remember:
{memory_context}

User: {message}
Assistant:"""

    # 3. Stream response
    return StreamingResponse(
        llm_service.stream_response(full_prompt),
        media_type="text/event-stream"
    )