import cv2
import numpy as np
from app.core.config import settings


class ImagePreprocessor:
    """Preprocessing utilities for symmetry detection"""

    @staticmethod
    def resize_image(image: np.ndarray, target_size: tuple = None) -> np.ndarray:
        """Resize image to target size"""
        if target_size is None:
            target_size = settings.IMAGE_SIZE
        return cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)

    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """Normalize pixel values to [0, 1]"""
        return image.astype(np.float32) / 255.0

    @staticmethod
    def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
        """Convert image to grayscale"""
        if len(image.shape) == 3:
            return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        return image

    @staticmethod
    def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Apply Gaussian blur for noise reduction"""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    @staticmethod
    def detect_edges(image: np.ndarray, low_threshold: int = 50, high_threshold: int = 150) -> np.ndarray:
        """Detect edges using Canny edge detection"""
        gray = ImagePreprocessor.convert_to_grayscale(image)
        return cv2.Canny(gray, low_threshold, high_threshold)

    @staticmethod
    def enhance_contrast(image: np.ndarray) -> np.ndarray:
        """Enhance image contrast using CLAHE"""
        gray = ImagePreprocessor.convert_to_grayscale(image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # If original was color, convert back
        if len(image.shape) == 3:
            return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)
        return enhanced

    @staticmethod
    def prepare_for_model(image: np.ndarray) -> np.ndarray:
        """Complete preprocessing pipeline for ML model"""

        # Resize
        resized = ImagePreprocessor.resize_image(image)

        # Normalize
        normalized = ImagePreprocessor.normalize_image(resized)

        # Add batch dimension
        batched = np.expand_dims(normalized, axis=0)

        return batched

    @staticmethod
    def create_symmetry_map(image: np.ndarray) -> dict:
        """Create various representations for symmetry analysis"""

        gray = ImagePreprocessor.convert_to_grayscale(image)
        edges = ImagePreprocessor.detect_edges(image)
        blurred = ImagePreprocessor.apply_gaussian_blur(gray)

        return {
            "original": image,
            "grayscale": gray,
            "edges": edges,
            "blurred": blurred,
            "shape": image.shape
        }

    @staticmethod
    def extract_features(image: np.ndarray) -> np.ndarray:
        """Extract features for symmetry detection"""

        gray = ImagePreprocessor.convert_to_grayscale(image)

        # Compute HOG features (Histogram of Oriented Gradients)
        win_size = (64, 64)
        block_size = (16, 16)
        block_stride = (8, 8)
        cell_size = (8, 8)
        nbins = 9

        # Resize to compatible size
        resized = cv2.resize(gray, (128, 128))

        hog = cv2.HOGDescriptor(win_size, block_size, block_stride, cell_size, nbins)
        features = hog.compute(resized)

        return features.flatten()