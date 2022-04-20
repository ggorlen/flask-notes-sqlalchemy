from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String
from db import Base

@dataclass
class Note(Base):
    id: int
    content: str

    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)

