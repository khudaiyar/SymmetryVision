"""
Database models for storing analysis results
This is optional and for future use when you want to persist data in a database
Currently, the app works without a database (files are stored locally)
"""

from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings

# Create SQLAlchemy base
Base = declarative_base()

# Database engine (SQLite for development, can be changed to PostgreSQL for production)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class AnalysisRecord(Base):
    """Database model for symmetry analysis records"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True, nullable=False)
    original_filename = Column(String, nullable=False)
    original_image_path = Column(String, nullable=False)
    processed_image_path = Column(String, nullable=False)
    thumbnail_path = Column(String)

    # Symmetry metrics
    symmetry_score = Column(Float, nullable=False)
    has_vertical_symmetry = Column(Boolean, default=False)
    has_horizontal_symmetry = Column(Boolean, default=False)
    has_radial_symmetry = Column(Boolean, default=False)

    # Detected axes (stored as JSON)
    detected_axes = Column(JSON)
    detected_regions = Column(JSON)

    # Processing info
    processing_time = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Optional: User association (for future multi-user support)
    user_id = Column(String, nullable=True)


def init_db():
    """Initialize database - create all tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# NOTE: To use the database:
# 1. Uncomment sqlalchemy in requirements.txt
# 2. Run: python -c "from app.models.database import init_db; init_db()"
# 3. Update routes to save/load from database