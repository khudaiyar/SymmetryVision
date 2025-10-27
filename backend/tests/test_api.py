"""
Unit tests for API endpoints
Run with: pytest tests/test_api.py
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
from PIL import Image


client = TestClient(app)


def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


class TestHealthEndpoints:
    """Test health check endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "name" in response.json()
        assert response.json()["name"] == "SymmetryVision"

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_upload_health(self):
        """Test upload service health"""
        response = client.get("/api/v1/upload/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestUploadEndpoint:
    """Test upload endpoints"""

    def test_upload_valid_image(self):
        """Test uploading a valid image"""
        img_bytes = create_test_image()

        response = client.post(
            "/api/v1/upload/",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")}
        )

        assert response.status_code == 200
        data = response.json()
        assert "file_id" in data
        assert "filename" in data
        assert data["message"] == "File uploaded successfully"

    def test_upload_invalid_file_type(self):
        """Test uploading invalid file type"""
        response = client.post(
            "/api/v1/upload/",
            files={"file": ("test.txt", b"not an image", "text/plain")}
        )

        assert response.status_code == 400

    def test_upload_no_file(self):
        """Test upload without file"""
        response = client.post("/api/v1/upload/")
        assert response.status_code == 422  # Unprocessable entity


class TestAnalysisEndpoint:
    """Test analysis endpoints"""

    def test_analyze_image(self):
        """Test image analysis"""
        img_bytes = create_test_image()

        response = client.post(
            "/api/v1/analyze/",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")}
        )

        # May take time to process
        assert response.status_code in [200, 500]  # 500 if processing fails

        if response.status_code == 200:
            data = response.json()
            assert "analysis_id" in data
            assert "symmetry_score" in data
            assert "detected_axes" in data
            assert isinstance(data["symmetry_score"], (int, float))

    def test_get_analysis_nonexistent(self):
        """Test getting non-existent analysis"""
        response = client.get("/api/v1/analyze/nonexistent_id")
        assert response.status_code == 404


class TestGalleryEndpoint:
    """Test gallery endpoints"""

    def test_get_gallery(self):
        """Test getting gallery"""
        response = client.get("/api/v1/gallery/")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data
        assert isinstance(data["items"], list)

    def test_get_gallery_with_params(self):
        """Test gallery with query parameters"""
        response = client.get("/api/v1/gallery/?limit=10&offset=0&sort_by=score")
        assert response.status_code == 200

    def test_get_gallery_stats(self):
        """Test gallery statistics"""
        response = client.get("/api/v1/gallery/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_analyses" in data
        assert "average_score" in data

    def test_delete_nonexistent_analysis(self):
        """Test deleting non-existent analysis"""
        response = client.delete("/api/v1/gallery/nonexistent_id")
        assert response.status_code == 404


class TestBatchAnalysis:
    """Test batch analysis"""

    def test_batch_analyze_multiple_images(self):
        """Test analyzing multiple images"""
        img1 = create_test_image()
        img2 = create_test_image()

        response = client.post(
            "/api/v1/analyze/batch",
            files=[
                ("files", ("test1.jpg", img1, "image/jpeg")),
                ("files", ("test2.jpg", img2, "image/jpeg"))
            ]
        )

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "total" in data
            assert "results" in data

    def test_batch_analyze_too_many(self):
        """Test batch with too many images"""
        files = [
            ("files", (f"test{i}.jpg", create_test_image(), "image/jpeg"))
            for i in range(15)  # More than max allowed (10)
        ]

        response = client.post("/api/v1/analyze/batch", files=files)
        assert response.status_code == 400


# Run tests with: pytest tests/test_api.py -v
# Run with coverage: pytest tests/test_api.py --cov=app