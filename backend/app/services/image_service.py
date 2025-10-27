import os
import uuid
import aiofiles
from fastapi import UploadFile
from PIL import Image
import cv2
import numpy as np
from app.core.config import settings
from datetime import datetime


class ImageService:
    """Service for handling image file operations"""

    @staticmethod
    def generate_file_id() -> str:
        """Generate unique file ID"""
        return str(uuid.uuid4())

    @staticmethod
    async def save_upload(file: UploadFile, content: bytes) -> dict:
        """Save uploaded file and return metadata"""

        # Generate unique filename
        file_id = ImageService.generate_file_id()
        file_ext = os.path.splitext(file.filename)[1]
        new_filename = f"{file_id}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, new_filename)

        # Save file asynchronously
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        return {
            "file_id": file_id,
            "filename": new_filename,
            "original_filename": file.filename,
            "file_path": file_path,
            "upload_time": datetime.now()
        }

    @staticmethod
    def load_image(file_path: str) -> np.ndarray:
        """Load image as numpy array"""
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError(f"Could not load image from {file_path}")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def save_processed_image(image: np.ndarray, file_id: str, suffix: str = "_processed") -> str:
        """Save processed image and return path"""

        filename = f"{file_id}{suffix}.jpg"
        file_path = os.path.join(settings.RESULTS_DIR, filename)

        # Convert RGB back to BGR for OpenCV
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(file_path, image_bgr)

        return file_path

    @staticmethod
    def get_image_dimensions(file_path: str) -> tuple:
        """Get image width and height"""
        with Image.open(file_path) as img:
            return img.size  # (width, height)

    @staticmethod
    def create_thumbnail(file_path: str, size: tuple = (300, 300)) -> str:
        """Create thumbnail and return path"""

        file_id = os.path.splitext(os.path.basename(file_path))[0]
        thumb_filename = f"{file_id}_thumb.jpg"
        thumb_path = os.path.join(settings.RESULTS_DIR, thumb_filename)

        with Image.open(file_path) as img:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumb_path, "JPEG")

        return thumb_path

    @staticmethod
    def cleanup_old_files(days: int = 7) -> int:
        """Remove files older than specified days"""

        count = 0
        current_time = datetime.now().timestamp()
        max_age = days * 24 * 60 * 60  # Convert days to seconds

        for directory in [settings.UPLOAD_DIR, settings.RESULTS_DIR]:
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                file_age = current_time - os.path.getmtime(file_path)

                if file_age > max_age:
                    os.remove(file_path)
                    count += 1

        return count

    @staticmethod
    def draw_symmetry_axis(image: np.ndarray, axis_data: dict) -> np.ndarray:
        """Draw symmetry axis on image"""

        img_copy = image.copy()
        coords = axis_data["coordinates"]

        # Draw line
        cv2.line(
            img_copy,
            (int(coords["x1"]), int(coords["y1"])),
            (int(coords["x2"]), int(coords["y2"])),
            color=(255, 0, 0),  # Red color
            thickness=3
        )

        # Add label
        label = f"{axis_data['type']} ({axis_data['confidence']:.2f})"
        cv2.putText(
            img_copy,
            label,
            (int(coords["x1"]) + 10, int(coords["y1"]) + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

        return img_copy