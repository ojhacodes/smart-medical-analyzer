from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

class Medication(BaseModel):
    name: str = Field(description="Name of the medication")
    dosage: str = Field(description="Dosage of the medication")
    frequency: str = Field(description="Frequency of taking the medication")
    duration: str = Field(description="Duration for the medication")

class AnalysisResponse(BaseModel):
    age: Optional[int] = Field(description="Age of the patient")
    gender: Literal["Male", "Female", "Unknown"] = Field(description="Gender of the patient")
    symptoms: List[str] = Field(description="List of symptoms")
    medications: List[Medication] = Field(description="List of prescribed medications")
    advice: Optional[str] = Field(description="General advice or notes")

class AnalyzeRequest(BaseModel):
    notes: str = Field(..., description="Raw unstructured notes from the physician")

class MedicalRecordResponse(AnalysisResponse):
    id: int
    raw_notes: str
    created_at: datetime

    class Config:
        from_attributes = True
