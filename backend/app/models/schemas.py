from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class SymmetryAxis(BaseModel):
    """Represents a detected symmetry axis"""
    type: str = Field(..., description="Type of symmetry: vertical, horizontal, diagonal")
    angle: float = Field(..., description="Angle of the axis in degrees")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    coordinates: Dict[str, float] = Field(..., description="Start and end points of the axis")


class SymmetryRegion(BaseModel):
    """Represents a symmetric region in the image"""
    region_id: int
    symmetry_type: str = Field(..., description="radial, reflective, rotational")
    center_x: float
    center_y: float
    confidence: float = Field(..., ge=0, le=1)


class SymmetryAnalysisResult(BaseModel):
    """Complete symmetry analysis result"""
    analysis_id: str = Field(..., description="Unique analysis ID")
    original_image_url: str
    processed_image_url: str
    symmetry_score: float = Field(..., ge=0, le=100, description="Overall symmetry score (0-100)")
    detected_axes: List[SymmetryAxis]
    detected_regions: List[SymmetryRegion]
    has_vertical_symmetry: bool
    has_horizontal_symmetry: bool
    has_radial_symmetry: bool
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "abc123xyz",
                "original_image_url": "/uploads/image.jpg",
                "processed_image_url": "/results/image_analyzed.jpg",
                "symmetry_score": 87.5,
                "detected_axes": [
                    {
                        "type": "vertical",
                        "angle": 90.0,
                        "confidence": 0.95,
                        "coordinates": {"x1": 250, "y1": 0, "x2": 250, "y2": 500}
                    }
                ],
                "detected_regions": [],
                "has_vertical_symmetry": True,
                "has_horizontal_symmetry": False,
                "has_radial_symmetry": False,
                "processing_time": 1.23,
                "timestamp": "2025-10-18T10:30:00"
            }
        }


class UploadResponse(BaseModel):
    """Response after successful image upload"""
    message: str
    file_id: str
    filename: str
    file_path: str


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None


class GalleryItem(BaseModel):
    """Gallery item for listing past analyses"""
    analysis_id: str
    thumbnail_url: str
    symmetry_score: float
    timestamp: datetime
    has_vertical_symmetry: bool
    has_horizontal_symmetry: bool


class GalleryResponse(BaseModel):
    """Gallery listing response"""
    total: int
    items: List[GalleryItem]