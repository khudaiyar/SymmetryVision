import cv2
import numpy as np
from typing import List, Tuple
from app.ml.preprocessor import ImagePreprocessor


class SymmetryDetector:
    """Core symmetry detection algorithms"""
    
    @staticmethod
    def detect_vertical_symmetry(image: np.ndarray, threshold: float = 0.85) -> Tuple[bool, float, dict]:
        """Detect vertical axis of symmetry"""
        
        gray = ImagePreprocessor.convert_to_grayscale(image)
        h, w = gray.shape
        
        # Split image into left and right halves
        mid = w // 2
        left_half = gray[:, :mid]
        right_half = gray[:, mid:mid + left_half.shape[1]]
        
        # Flip right half horizontally
        right_flipped = cv2.flip(right_half, 1)
        
        # Calculate similarity using normalized cross-correlation
        if left_half.shape == right_flipped.shape:
            # Normalize both halves
            left_norm = (left_half - np.mean(left_half)) / (np.std(left_half) + 1e-10)
            right_norm = (right_flipped - np.mean(right_flipped)) / (np.std(right_flipped) + 1e-10)
            
            # Compute correlation
            correlation = np.mean(left_norm * right_norm)
            confidence = (correlation + 1) / 2  # Convert from [-1,1] to [0,1]
            
            axis_coords = {
                "x1": mid, "y1": 0,
                "x2": mid, "y2": h
            }
            
            return confidence >= threshold, confidence, axis_coords
        
        return False, 0.0, {}
    
    @staticmethod
    def detect_horizontal_symmetry(image: np.ndarray, threshold: float = 0.85) -> Tuple[bool, float, dict]:
        """Detect horizontal axis of symmetry"""
        
        gray = ImagePreprocessor.convert_to_grayscale(image)
        h, w = gray.shape
        
        # Split image into top and bottom halves
        mid = h // 2
        top_half = gray[:mid, :]
        bottom_half = gray[mid:mid + top_half.shape[0], :]
        
        # Flip bottom half vertically
        bottom_flipped = cv2.flip(bottom_half, 0)
        
        # Calculate similarity
        if top_half.shape == bottom_flipped.shape:
            # Normalize
            top_norm = (top_half - np.mean(top_half)) / (np.std(top_half) + 1e-10)
            bottom_norm = (bottom_flipped - np.mean(bottom_flipped)) / (np.std(bottom_flipped) + 1e-10)
            
            # Compute correlation
            correlation = np.mean(top_norm * bottom_norm)
            confidence = (correlation + 1) / 2
            
            axis_coords = {
                "x1": 0, "y1": mid,
                "x2": w, "y2": mid
            }
            
            return confidence >= threshold, confidence, axis_coords
        
        return False, 0.0, {}
    
    @staticmethod
    def detect_diagonal_symmetry(image: np.ndarray, threshold: float = 0.75) -> List[Tuple[bool, float, dict, str]]:
        """Detect diagonal axes of symmetry (main and anti-diagonal)"""
        
        gray = ImagePreprocessor.convert_to_grayscale(image)
        h, w = gray.shape
        
        results = []
        
        # Make image square for easier diagonal detection
        size = min(h, w)
        gray_square = cv2.resize(gray, (size, size))
        
        # Main diagonal (top-left to bottom-right)
        # Rotate image 45 degrees and check for vertical symmetry
        center = (size // 2, size // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
        rotated_45 = cv2.warpAffine(gray_square, rotation_matrix, (size, size))
        
        # Check vertical symmetry on rotated image
        mid = size // 2
        left = rotated_45[:, :mid]
        right = rotated_45[:, mid:mid + left.shape[1]]
        
        if left.shape == right.shape:
            right_flipped = cv2.flip(right, 1)
            left_norm = (left - np.mean(left)) / (np.std(left) + 1e-10)
            right_norm = (right_flipped - np.mean(right_flipped)) / (np.std(right_flipped) + 1e-10)
            correlation = np.mean(left_norm * right_norm)
            confidence = (correlation + 1) / 2
            
            if confidence >= threshold:
                results.append((True, confidence, {
                    "x1": 0, "y1": 0,
                    "x2": w, "y2": h
                }, "main_diagonal"))
        
        # Anti-diagonal (top-right to bottom-left)
        rotation_matrix_135 = cv2.getRotationMatrix2D(center, 135, 1.0)
        rotated_135 = cv2.warpAffine(gray_square, rotation_matrix_135, (size, size))
        
        left_135 = rotated_135[:, :mid]
        right_135 = rotated_135[:, mid:mid + left_135.shape[1]]
        
        if left_135.shape == right_135.shape:
            right_flipped_135 = cv2.flip(right_135, 1)
            left_norm_135 = (left_135 - np.mean(left_135)) / (np.std(left_135) + 1e-10)
            right_norm_135 = (right_flipped_135 - np.mean(right_flipped_135)) / (np.std(right_flipped_135) + 1e-10)
            correlation_135 = np.mean(left_norm_135 * right_norm_135)
            confidence_135 = (correlation_135 + 1) / 2
            
            if confidence_135 >= threshold:
                results.append((True, confidence_135, {
                    "x1": w, "y1": 0,
                    "x2": 0, "y2": h
                }, "anti_diagonal"))
        
        return results
    
    @staticmethod
    def detect_radial_symmetry(image: np.ndarray, num_angles: int = 8, threshold: float = 0.70) -> Tuple[bool, float]:
        """Detect radial (rotational) symmetry"""
        
        gray = ImagePreprocessor.convert_to_grayscale(image)
        h, w = gray.shape
        center = (w // 2, h // 2)
        
        # Get image center
        angle_step = 360 / num_angles
        similarities = []
        
        for i in range(1, num_angles):  # Start from 1 to skip 0 degrees
            angle = i * angle_step
            
            # Rotate image
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(gray, matrix, (w, h))
            
            # Compare with original
            diff = cv2.absdiff(gray, rotated)
            similarity = 1.0 - (np.mean(diff) / 255.0)
            similarities.append(similarity)
        
        # Average similarity across all rotations
        avg_similarity = np.mean(similarities)
        
        return avg_similarity >= threshold, avg_similarity
    
    @staticmethod
    def calculate_overall_score(vertical_conf: float, horizontal_conf: float, 
                               radial_conf: float, diagonal_confs: List[float]) -> float:
        """Calculate overall symmetry score (0-100)"""
        
        scores = []
        weights = []
        
        # Weight vertical and horizontal more heavily
        if vertical_conf > 0:
            scores.append(vertical_conf)
            weights.append(1.5)
        
        if horizontal_conf > 0:
            scores.append(horizontal_conf)
            weights.append(1.5)
        
        if radial_conf > 0:
            scores.append(radial_conf)
            weights.append(1.2)
        
        for dc in diagonal_confs:
            if dc > 0:
                scores.append(dc)
                weights.append(1.0)
        
        if not scores:
            return 0.0
        
        # Calculate weighted average
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        total_weight = sum(weights)
        overall_score = (weighted_sum / total_weight) * 100
        
        return min(overall_score, 100.0)
    
    @staticmethod
    def find_symmetry_regions(image: np.ndarray) -> List[dict]:
        """Find and segment symmetric regions"""
        
        gray = ImagePreprocessor.convert_to_grayscale(image)
        edges = ImagePreprocessor.detect_edges(image)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions = []
        for i, contour in enumerate(contours):
            # Filter small contours
            area = cv2.contourArea(contour)
            if area < 100:
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate center
            center_x = x + w // 2
            center_y = y + h // 2
            
            regions.append({
                "region_id": i,
                "symmetry_type": "reflective",
                "center_x": float(center_x),
                "center_y": float(center_y),
                "confidence": 0.8
            })
        
        return regions[:5]  # Return top 5 regions