import time
from typing import List
import numpy as np
from app.ml.detector import SymmetryDetector
from app.ml.preprocessor import ImagePreprocessor
from app.services.image_service import ImageService
from app.models.schemas import (
    SymmetryAnalysisResult,
    SymmetryAxis,
    SymmetryRegion
)
from datetime import datetime


class SymmetryService:
    """Main service for symmetry detection and analysis"""

    def __init__(self):
        self.detector = SymmetryDetector()
        self.preprocessor = ImagePreprocessor()
        self.image_service = ImageService()

    async def analyze_image(self, file_path: str, file_id: str) -> SymmetryAnalysisResult:
        """Complete symmetry analysis pipeline"""

        start_time = time.time()

        # Load image
        image = self.image_service.load_image(file_path)

        # Detect symmetries
        detected_axes = []
        diagonal_confs = []

        # Vertical symmetry
        has_vert, vert_conf, vert_coords = self.detector.detect_vertical_symmetry(image)
        if has_vert:
            detected_axes.append(SymmetryAxis(
                type="vertical",
                angle=90.0,
                confidence=float(vert_conf),
                coordinates=vert_coords
            ))

        # Horizontal symmetry
        has_horiz, horiz_conf, horiz_coords = self.detector.detect_horizontal_symmetry(image)
        if has_horiz:
            detected_axes.append(SymmetryAxis(
                type="horizontal",
                angle=0.0,
                confidence=float(horiz_conf),
                coordinates=horiz_coords
            ))

        # Diagonal symmetry
        diagonal_results = self.detector.detect_diagonal_symmetry(image)
        for has_diag, diag_conf, diag_coords, diag_type in diagonal_results:
            detected_axes.append(SymmetryAxis(
                type=diag_type,
                angle=45.0 if diag_type == "main_diagonal" else 135.0,
                confidence=float(diag_conf),
                coordinates=diag_coords
            ))
            diagonal_confs.append(diag_conf)

        # Radial symmetry
        has_radial, radial_conf = self.detector.detect_radial_symmetry(image)

        # Find symmetric regions
        regions_data = self.detector.find_symmetry_regions(image)
        detected_regions = [
            SymmetryRegion(**region) for region in regions_data
        ]

        # Calculate overall symmetry score
        symmetry_score = self.detector.calculate_overall_score(
            vert_conf if has_vert else 0.0,
            horiz_conf if has_horiz else 0.0,
            radial_conf if has_radial else 0.0,
            diagonal_confs
        )

        # Draw symmetry axes on image
        processed_image = image.copy()
        for axis in detected_axes:
            processed_image = self.image_service.draw_symmetry_axis(
                processed_image,
                axis.model_dump()
            )

        # Save processed image
        processed_path = self.image_service.save_processed_image(
            processed_image,
            file_id,
            "_analyzed"
        )

        # Create thumbnail
        thumbnail_path = self.image_service.create_thumbnail(file_path)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Build result
        result = SymmetryAnalysisResult(
            analysis_id=file_id,
            original_image_url=f"/uploads/{file_id}",
            processed_image_url=f"/results/{file_id}_analyzed.jpg",
            symmetry_score=float(symmetry_score),
            detected_axes=detected_axes,
            detected_regions=detected_regions,
            has_vertical_symmetry=has_vert,
            has_horizontal_symmetry=has_horiz,
            has_radial_symmetry=has_radial,
            processing_time=processing_time,
            timestamp=datetime.now()
        )

        return result

    def get_analysis_summary(self, result: SymmetryAnalysisResult) -> dict:
        """Generate human-readable summary"""

        summary = {
            "overall_assessment": self._get_assessment_text(result.symmetry_score),
            "dominant_symmetry": self._get_dominant_symmetry(result),
            "symmetry_count": len(result.detected_axes),
            "confidence_level": self._get_confidence_level(result.detected_axes)
        }

        return summary

    def _get_assessment_text(self, score: float) -> str:
        """Get text assessment based on score"""
        if score >= 90:
            return "Highly symmetric"
        elif score >= 75:
            return "Strongly symmetric"
        elif score >= 60:
            return "Moderately symmetric"
        elif score >= 40:
            return "Somewhat symmetric"
        else:
            return "Low symmetry"

    def _get_dominant_symmetry(self, result: SymmetryAnalysisResult) -> str:
        """Determine dominant type of symmetry"""
        if not result.detected_axes:
            return "None"

        # Find axis with highest confidence
        dominant = max(result.detected_axes, key=lambda x: x.confidence)
        return dominant.type

    def _get_confidence_level(self, axes: List[SymmetryAxis]) -> str:
        """Calculate average confidence level"""
        if not axes:
            return "None"

        avg_conf = sum(axis.confidence for axis in axes) / len(axes)

        if avg_conf >= 0.9:
            return "Very High"
        elif avg_conf >= 0.75:
            return "High"
        elif avg_conf >= 0.6:
            return "Moderate"
        else:
            return "Low"