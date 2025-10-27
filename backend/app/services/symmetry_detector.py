"""
Symmetry Detector Service
High-level service for symmetry detection operations
"""

import numpy as np
import cv2
from typing import Dict, List, Tuple
from app.ml.detector import SymmetryDetector
from app.ml.preprocessor import ImagePreprocessor


class SymmetryDetectorService:
    """
    Service layer for symmetry detection
    Wraps the ML detector with additional business logic
    """

    def __init__(self):
        self.detector = SymmetryDetector()
        self.preprocessor = ImagePreprocessor()

    def detect_all_symmetries(self, image: np.ndarray) -> Dict:
        """
        Detect all types of symmetry in an image

        Args:
            image: Input image as numpy array (RGB)

        Returns:
            Dictionary containing all symmetry detection results
        """

        results = {
            "vertical": {},
            "horizontal": {},
            "diagonal": [],
            "radial": {},
            "overall_score": 0.0
        }

        # Detect vertical symmetry
        has_vert, vert_conf, vert_coords = self.detector.detect_vertical_symmetry(image)
        results["vertical"] = {
            "detected": has_vert,
            "confidence": float(vert_conf),
            "coordinates": vert_coords
        }

        # Detect horizontal symmetry
        has_horiz, horiz_conf, horiz_coords = self.detector.detect_horizontal_symmetry(image)
        results["horizontal"] = {
            "detected": has_horiz,
            "confidence": float(horiz_conf),
            "coordinates": horiz_coords
        }

        # Detect diagonal symmetry
        diagonal_results = self.detector.detect_diagonal_symmetry(image)
        for has_diag, diag_conf, diag_coords, diag_type in diagonal_results:
            results["diagonal"].append({
                "type": diag_type,
                "detected": has_diag,
                "confidence": float(diag_conf),
                "coordinates": diag_coords
            })

        # Detect radial symmetry
        has_radial, radial_conf = self.detector.detect_radial_symmetry(image)
        results["radial"] = {
            "detected": has_radial,
            "confidence": float(radial_conf)
        }

        # Calculate overall score
        diagonal_confs = [d["confidence"] for d in results["diagonal"]]
        overall_score = self.detector.calculate_overall_score(
            vert_conf if has_vert else 0.0,
            horiz_conf if has_horiz else 0.0,
            radial_conf if has_radial else 0.0,
            diagonal_confs
        )
        results["overall_score"] = float(overall_score)

        return results

    def quick_symmetry_check(self, image: np.ndarray) -> Dict:
        """
        Quick symmetry check (only vertical and horizontal)
        Faster than full detection

        Args:
            image: Input image

        Returns:
            Basic symmetry information
        """

        has_vert, vert_conf, _ = self.detector.detect_vertical_symmetry(image)
        has_horiz, horiz_conf, _ = self.detector.detect_horizontal_symmetry(image)

        return {
            "has_symmetry": has_vert or has_horiz,
            "vertical_confidence": float(vert_conf),
            "horizontal_confidence": float(horiz_conf),
            "quick_score": float((vert_conf + horiz_conf) / 2 * 100)
        }

    def compare_symmetry(self, image1: np.ndarray, image2: np.ndarray) -> Dict:
        """
        Compare symmetry between two images

        Args:
            image1: First image
            image2: Second image

        Returns:
            Comparison results
        """

        results1 = self.detect_all_symmetries(image1)
        results2 = self.detect_all_symmetries(image2)

        return {
            "image1_score": results1["overall_score"],
            "image2_score": results2["overall_score"],
            "difference": abs(results1["overall_score"] - results2["overall_score"]),
            "more_symmetric": "image1" if results1["overall_score"] > results2["overall_score"] else "image2"
        }

    def get_symmetry_report(self, image: np.ndarray) -> str:
        """
        Generate human-readable symmetry report

        Args:
            image: Input image

        Returns:
            Formatted text report
        """

        results = self.detect_all_symmetries(image)

        report = []
        report.append("=" * 50)
        report.append("SYMMETRY ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"\nOverall Symmetry Score: {results['overall_score']:.2f}/100")
        report.append("\nDetected Symmetries:")
        report.append("-" * 50)

        # Vertical
        if results["vertical"]["detected"]:
            conf = results["vertical"]["confidence"] * 100
            report.append(f"✓ Vertical Symmetry (Confidence: {conf:.1f}%)")
        else:
            report.append("✗ No Vertical Symmetry")

        # Horizontal
        if results["horizontal"]["detected"]:
            conf = results["horizontal"]["confidence"] * 100
            report.append(f"✓ Horizontal Symmetry (Confidence: {conf:.1f}%)")
        else:
            report.append("✗ No Horizontal Symmetry")

        # Diagonal
        if results["diagonal"]:
            for diag in results["diagonal"]:
                conf = diag["confidence"] * 100
                report.append(f"✓ {diag['type'].replace('_', ' ').title()} (Confidence: {conf:.1f}%)")
        else:
            report.append("✗ No Diagonal Symmetry")

        # Radial
        if results["radial"]["detected"]:
            conf = results["radial"]["confidence"] * 100
            report.append(f"✓ Radial Symmetry (Confidence: {conf:.1f}%)")
        else:
            report.append("✗ No Radial Symmetry")

        report.append("=" * 50)

        return "\n".join(report)

    def validate_symmetry_threshold(self, image: np.ndarray, min_score: float = 70.0) -> bool:
        """
        Check if image meets minimum symmetry threshold

        Args:
            image: Input image
            min_score: Minimum required score (0-100)

        Returns:
            True if image meets threshold
        """

        results = self.detect_all_symmetries(image)
        return results["overall_score"] >= min_score

    def get_dominant_symmetry_type(self, image: np.ndarray) -> str:
        """
        Get the dominant type of symmetry in the image

        Args:
            image: Input image

        Returns:
            Name of dominant symmetry type
        """

        results = self.detect_all_symmetries(image)

        confidences = {
            "vertical": results["vertical"]["confidence"],
            "horizontal": results["horizontal"]["confidence"],
            "radial": results["radial"]["confidence"]
        }

        # Add diagonal
        for diag in results["diagonal"]:
            confidences[diag["type"]] = diag["confidence"]

        if not confidences or max(confidences.values()) == 0:
            return "none"

        return max(confidences, key=confidences.get)

    def batch_detect(self, images: List[np.ndarray]) -> List[Dict]:
        """
        Detect symmetry in multiple images

        Args:
            images: List of images

        Returns:
            List of detection results
        """

        results = []
        for i, image in enumerate(images):
            try:
                result = self.detect_all_symmetries(image)
                result["image_index"] = i
                result["success"] = True
                results.append(result)
            except Exception as e:
                results.append({
                    "image_index": i,
                    "success": False,
                    "error": str(e)
                })

        return results


# Global instance (singleton)
_detector_service_instance = None


def get_symmetry_detector_service() -> SymmetryDetectorService:
    """Get or create symmetry detector service instance"""
    global _detector_service_instance

    if _detector_service_instance is None:
        _detector_service_instance = SymmetryDetectorService()

    return _detector_service_instance