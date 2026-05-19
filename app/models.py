from sqlalchemy import Column, Integer, String, JSON, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    raw_notes = Column(Text, nullable=False)
    
    # Structured data
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    symptoms = Column(JSON, nullable=True)
    medications = Column(JSON, nullable=True)
    advice = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
