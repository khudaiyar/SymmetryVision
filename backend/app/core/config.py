from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings and configuration"""

    # Application
    APP_NAME: str = "SymmetryVision"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

    # File Storage
    UPLOAD_DIR: str = "uploads"
    RESULTS_DIR: str = "results"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".bmp"]

    # ML Model
    MODEL_PATH: str = "models/symmetry_detector.h5"
    CONFIDENCE_THRESHOLD: float = 0.7
    IMAGE_SIZE: tuple = (224, 224)

    # Database (optional - for future use)
    DATABASE_URL: str = "sqlite:///./symmetry_vision.db"

    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.RESULTS_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)


# Global settings instance
settings = Settings()