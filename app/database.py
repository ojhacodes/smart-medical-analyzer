import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Check if a database URL is provided (e.g., from Render/Railway)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # If using PostgreSQL, we might need to change 'postgres://' to 'postgresql://' (SQLAlchemy 1.4+ requirement)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Connect to PostgreSQL without the SQLite specific thread arguments
    engine = create_engine(DATABASE_URL)
else:
    # Fallback to local SQLite for development
    DATABASE_URL = "sqlite:///./medical_analyzer.db"
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
