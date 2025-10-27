from fastapi import HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import os


def setup_cors(app):
    """Configure CORS middleware"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file"""

    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Check content type
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )


async def validate_file_size(file: UploadFile) -> None:
    """Validate file size (must be called after reading file)"""

    # Read file content to check size
    content = await file.read()
    size = len(content)

    if size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )

    # Reset file pointer to beginning
    await file.seek(0)

    return content