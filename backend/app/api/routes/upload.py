from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.security import validate_image_file, validate_file_size
from app.services.image_service import ImageService
from app.models.schemas import UploadResponse, ErrorResponse


router = APIRouter(prefix="/upload", tags=["Upload"])
image_service = ImageService()


@router.post("/", response_model=UploadResponse, summary="Upload an image for analysis")
async def upload_image(
        file: UploadFile = File(..., description="Image file to analyze")
):
    """
    Upload an image file for symmetry analysis.

    - **file**: Image file (JPG, JPEG, PNG, BMP)
    - Returns: File metadata including unique file ID
    """

    try:
        # Validate file type
        validate_image_file(file)

        # Validate file size
        content = await validate_file_size(file)

        # Save file
        file_metadata = await image_service.save_upload(file, content)

        return UploadResponse(
            message="File uploaded successfully",
            file_id=file_metadata["file_id"],
            filename=file_metadata["filename"],
            file_path=file_metadata["file_path"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/health", summary="Check upload service health")
async def health_check():
    """Health check endpoint for upload service"""
    return {
        "status": "healthy",
        "service": "upload",
        "message": "Upload service is running"
    }