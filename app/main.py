from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import os

from . import models, schemas, database, analyzer

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Smart Medical Text Analyzer",
    description="Extracts structured medical data from raw physician notes.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/analyze", response_model=schemas.MedicalRecordResponse)
def analyze_notes(request: schemas.AnalyzeRequest, db: Session = Depends(database.get_db)):
    # 1. Analyze text with NLP component
    extracted_data = analyzer.analyze_medical_notes(request.notes)
    
    # Validate with Pydantic (will raise validation error if schema doesn't match)
    try:
        validated_data = schemas.AnalysisResponse(**extracted_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extracted data failed validation: {e}")
        
    # 2. Save to database
    db_record = models.MedicalRecord(
        raw_notes=request.notes,
        age=validated_data.age,
        gender=validated_data.gender,
        symptoms=validated_data.symptoms,
        medications=[m.model_dump() for m in validated_data.medications],
        advice=validated_data.advice
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    return db_record

@app.get("/history", response_model=List[schemas.MedicalRecordResponse])
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    records = db.query(models.MedicalRecord).offset(skip).limit(limit).all()
    return records
