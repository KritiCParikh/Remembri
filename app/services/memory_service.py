# app/services/memory_service.py
from sqlalchemy.orm import Session
from app.models.memory import Memory
from sqlalchemy import or_

# Create/Add memory
def create_memory(db: Session, content: str, type_: str, key: str):
    db_memory = Memory(content=content, type=type_, key=key)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

# Get all memories
def get_memories(db: Session):
    return db.query(Memory).all()

# Get memory by key
def get_memory_by_key(db: Session, key: str):
    return db.query(Memory).filter(Memory.key == key).first()

# Search memories by type
def search_memories_by_type(db: Session, type_: str):
    return db.query(Memory).filter(Memory.type == type_).all()

# Search memories by content or key
def search_memories(db: Session, query: str):
    return db.query(Memory).filter(
        or_(
            Memory.content.like(f"%{query}%"),
            Memory.key.like(f"%{query}%")
        )
    ).all()

# Update memory content by key
def update_memory(db: Session, key: str, new_content: str):
    memory = db.query(Memory).filter(Memory.key == key).first()
    if memory:
        memory.content = new_content
        db.commit()
        db.refresh(memory)
    return memory
