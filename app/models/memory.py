# app/models/memory.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class Memory(Base):
    __tablename__ = 'memories'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)
    key = Column(String, nullable=False)