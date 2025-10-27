from typing import Optional
from fastapi import Depends, HTTPException, status
from app.services.symmetry_service import SymmetryService
from app.services.image_service import ImageService


def get_symmetry_service() -> SymmetryService:
    """Dependency to get SymmetryService instance"""
    return SymmetryService()


def get_image_service() -> ImageService:
    """Dependency to get ImageService instance"""
    return ImageService()


# Optional: Add authentication dependency for future use
async def get_current_user(token: Optional[str] = None):
    """
    Get current user from token (placeholder for future authentication)
    For now, returns None (no authentication required)
    """
    # TODO: Implement JWT token validation when authentication is added
    return None