from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import SessionLocal
from app.services import memory_service

router = APIRouter(prefix="/memory", tags=["memory"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Models
class AddMemoryRequest(BaseModel):
    type: str
    key: str
    content: str

class UpdateMemoryRequest(BaseModel):
    key: str
    new_content: str

# Add Memory
@router.post("/add")
def add_memory(request: AddMemoryRequest, db: Session = Depends(get_db)):
    memory = memory_service.create_memory(db, request.content, request.type, request.key)
    return {"message": "Memory added", "memory": memory}

# Get Memory by key
@router.get("/get/{key}")
def get_memory(key: str, db: Session = Depends(get_db)):
    memory = memory_service.get_memory_by_key(db, key)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory

# List all Memories
@router.get("/list")
def list_memories(db: Session = Depends(get_db)):
    memories = memory_service.get_memories(db)
    return memories

# Search Memories by content/key
@router.get("/search")
def search_memories(query: str, db: Session = Depends(get_db)):
    results = memory_service.search_memories(db, query)
    return results

# Update Memory
@router.put("/update")
def update_memory(request: UpdateMemoryRequest, db: Session = Depends(get_db)):
    memory = memory_service.update_memory(db, request.key, request.new_content)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"message": "Memory updated", "memory": memory}

