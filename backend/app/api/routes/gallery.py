from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.models.schemas import GalleryResponse, GalleryItem
from app.core.config import settings
import os
from datetime import datetime
from typing import Optional


router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("/", response_model=GalleryResponse, summary="Get gallery of analyzed images")
async def get_gallery(
        limit: int = Query(default=20, ge=1, le=100, description="Number of items to return"),
        offset: int = Query(default=0, ge=0, description="Number of items to skip"),
        sort_by: str = Query(default="timestamp", description="Sort by: timestamp, score")
):
    """
    Retrieve gallery of previously analyzed images.

    - **limit**: Maximum number of items (1-100)
    - **offset**: Skip first N items for pagination
    - **sort_by**: Sort order (timestamp or score)
    - Returns: List of gallery items with thumbnails
    """

    try:
        items = []
        results_dir = settings.RESULTS_DIR

        # Get all analyzed images
        if not os.path.exists(results_dir):
            return GalleryResponse(total=0, items=[])

        files = os.listdir(results_dir)
        analyzed_files = [f for f in files if f.endswith("_analyzed.jpg")]

        for filename in analyzed_files:
            file_id = filename.replace("_analyzed.jpg", "")
            file_path = os.path.join(results_dir, filename)
            thumb_path = os.path.join(results_dir, f"{file_id}_thumb.jpg")

            # Get file metadata
            stat = os.stat(file_path)
            timestamp = datetime.fromtimestamp(stat.st_mtime)

            # For now, use placeholder score (in production, load from database)
            score = 75.0  # TODO: Load actual score from database

            items.append(GalleryItem(
                analysis_id=file_id,
                thumbnail_url=f"/results/{file_id}_thumb.jpg" if os.path.exists(thumb_path) else f"/results/{filename}",
                symmetry_score=score,
                timestamp=timestamp,
                has_vertical_symmetry=True,  # TODO: Load from database
                has_horizontal_symmetry=False
            ))

        # Sort items
        if sort_by == "score":
            items.sort(key=lambda x: x.symmetry_score, reverse=True)
        else:  # timestamp
            items.sort(key=lambda x: x.timestamp, reverse=True)

        # Apply pagination
        total = len(items)
        items = items[offset:offset + limit]

        return GalleryResponse(total=total, items=items)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load gallery: {str(e)}"
        )


@router.get("/image/{filename}", summary="Serve gallery image")
async def get_gallery_image(filename: str):
    """
    Serve an image file from the gallery.

    - **filename**: Name of the image file
    - Returns: Image file
    """

    # Check in results directory
    file_path = os.path.join(settings.RESULTS_DIR, filename)

    if not os.path.exists(file_path):
        # Try uploads directory
        file_path = os.path.join(settings.UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path)


@router.delete("/{file_id}", summary="Delete analysis from gallery")
async def delete_analysis(file_id: str):
    """
    Delete an analysis and its associated files.

    - **file_id**: Analysis identifier
    - Returns: Deletion confirmation
    """

    deleted_files = []

    # Delete from uploads
    for ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        upload_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(upload_path):
            os.remove(upload_path)
            deleted_files.append(upload_path)

    # Delete from results
    result_patterns = [
        f"{file_id}_analyzed.jpg",
        f"{file_id}_thumb.jpg",
        f"{file_id}_processed.jpg"
    ]

    for pattern in result_patterns:
        result_path = os.path.join(settings.RESULTS_DIR, pattern)
        if os.path.exists(result_path):
            os.remove(result_path)
            deleted_files.append(result_path)

    if not deleted_files:
        raise HTTPException(
            status_code=404,
            detail=f"No files found for analysis ID: {file_id}"
        )

    return {
        "message": "Analysis deleted successfully",
        "file_id": file_id,
        "deleted_files": len(deleted_files)
    }


@router.get("/stats", summary="Get gallery statistics")
async def get_gallery_stats():
    """
    Get statistics about analyzed images.

    - Returns: Statistics summary
    """

    results_dir = settings.RESULTS_DIR

    if not os.path.exists(results_dir):
        return {
            "total_analyses": 0,
            "average_score": 0,
            "highest_score": 0,
            "lowest_score": 0
        }

    files = os.listdir(results_dir)
    analyzed_files = [f for f in files if f.endswith("_analyzed.jpg")]

    # TODO: Calculate actual statistics from database
    return {
        "total_analyses": len(analyzed_files),
        "average_score": 72.5,  # Placeholder
        "highest_score": 95.0,
        "lowest_score": 45.0,
        "storage_used_mb": sum(
            os.path.getsize(os.path.join(results_dir, f))
            for f in files
        ) / (1024 * 1024)
    }