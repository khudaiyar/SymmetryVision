from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.symmetry_service import SymmetryService
from app.services.image_service import ImageService
from app.models.schemas import SymmetryAnalysisResult, ErrorResponse
from app.core.security import validate_image_file, validate_file_size
import os
from app.core.config import settings


router = APIRouter(prefix="/analyze", tags=["Analysis"])
symmetry_service = SymmetryService()
image_service = ImageService()


@router.post("/", response_model=SymmetryAnalysisResult, summary="Analyze image symmetry")
async def analyze_symmetry(
        file: UploadFile = File(..., description="Image file to analyze")
):
    """
    Analyze symmetry in an uploaded image.

    This endpoint:
    1. Uploads and validates the image
    2. Detects vertical, horizontal, diagonal, and radial symmetry
    3. Calculates symmetry score (0-100)
    4. Returns annotated image with symmetry axes highlighted

    - **file**: Image file (JPG, JPEG, PNG, BMP)
    - Returns: Complete symmetry analysis result
    """

    try:
        # Validate file
        validate_image_file(file)
        content = await validate_file_size(file)

        # Save uploaded file
        file_metadata = await image_service.save_upload(file, content)
        file_id = file_metadata["file_id"]
        file_path = file_metadata["file_path"]

        # Perform symmetry analysis
        result = await symmetry_service.analyze_image(file_path, file_id)

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/{file_id}", response_model=SymmetryAnalysisResult, summary="Get analysis by ID")
async def get_analysis(file_id: str):
    """
    Retrieve existing analysis result by file ID.

    - **file_id**: Unique identifier for the analyzed image
    - Returns: Previously computed symmetry analysis
    """

    # Check if files exist
    upload_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.jpg")
    result_path = os.path.join(settings.RESULTS_DIR, f"{file_id}_analyzed.jpg")

    if not os.path.exists(upload_path):
        # Try other extensions
        for ext in [".png", ".jpeg", ".bmp"]:
            alt_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(alt_path):
                upload_path = alt_path
                break
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Analysis with ID '{file_id}' not found"
            )

    # Re-analyze if processed image doesn't exist
    if not os.path.exists(result_path):
        result = await symmetry_service.analyze_image(upload_path, file_id)
        return result

    # TODO: Load from database or cache if available
    # For now, re-run analysis
    result = await symmetry_service.analyze_image(upload_path, file_id)
    return result


@router.post("/batch", summary="Batch analyze multiple images")
async def batch_analyze(files: list[UploadFile] = File(...)):
    """
    Analyze multiple images in a single request.

    - **files**: List of image files
    - Returns: List of analysis results
    """

    if len(files) > 10:
        raise HTTPException(
            status_code=400,
            detail="Maximum 10 images allowed per batch"
        )

    results = []

    for file in files:
        try:
            # Validate and upload
            validate_image_file(file)
            content = await validate_file_size(file)
            file_metadata = await image_service.save_upload(file, content)

            # Analyze
            result = await symmetry_service.analyze_image(
                file_metadata["file_path"],
                file_metadata["file_id"]
            )
            results.append(result)

        except Exception as e:
            results.append({
                "error": str(e),
                "filename": file.filename
            })

    return {
        "total": len(files),
        "successful": len([r for r in results if not isinstance(r, dict) or "error" not in r]),
        "results": results
    }


@router.get("/summary/{file_id}", summary="Get analysis summary")
async def get_analysis_summary(file_id: str):
    """
    Get human-readable summary of symmetry analysis.

    - **file_id**: Analysis identifier
    - Returns: Text summary of findings
    """

    upload_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}.jpg")

    if not os.path.exists(upload_path):
        raise HTTPException(status_code=404, detail="Analysis not found")

    result = await symmetry_service.analyze_image(upload_path, file_id)
    summary = symmetry_service.get_analysis_summary(result)

    return {
        "file_id": file_id,
        "summary": summary,
        "details": result
    }