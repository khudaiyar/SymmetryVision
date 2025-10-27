import os
import shutil
from typing import List, Dict
from datetime import datetime, timedelta
from app.core.config import settings


class StorageService:
    """Service for managing file storage and cleanup"""

    @staticmethod
    def get_storage_stats() -> Dict:
        """Get storage statistics"""

        upload_size = 0
        results_size = 0
        upload_count = 0
        results_count = 0

        # Calculate uploads directory size
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                filepath = os.path.join(settings.UPLOAD_DIR, filename)
                if os.path.isfile(filepath):
                    upload_size += os.path.getsize(filepath)
                    upload_count += 1

        # Calculate results directory size
        if os.path.exists(settings.RESULTS_DIR):
            for filename in os.listdir(settings.RESULTS_DIR):
                filepath = os.path.join(settings.RESULTS_DIR, filename)
                if os.path.isfile(filepath):
                    results_size += os.path.getsize(filepath)
                    results_count += 1

        total_size = upload_size + results_size

        return {
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "upload_size_mb": round(upload_size / (1024 * 1024), 2),
            "results_size_mb": round(results_size / (1024 * 1024), 2),
            "upload_count": upload_count,
            "results_count": results_count,
            "total_files": upload_count + results_count
        }

    @staticmethod
    def cleanup_old_files(days: int = 7) -> Dict:
        """Remove files older than specified days"""

        current_time = datetime.now()
        max_age = timedelta(days=days)
        deleted_files = []

        for directory in [settings.UPLOAD_DIR, settings.RESULTS_DIR]:
            if not os.path.exists(directory):
                continue

            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)

                if not os.path.isfile(filepath):
                    continue

                # Get file modification time
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                file_age = current_time - file_time

                if file_age > max_age:
                    try:
                        os.remove(filepath)
                        deleted_files.append({
                            "filename": filename,
                            "directory": directory,
                            "age_days": file_age.days
                        })
                    except Exception as e:
                        print(f"Failed to delete {filepath}: {e}")

        return {
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files,
            "threshold_days": days
        }

    @staticmethod
    def delete_analysis_files(file_id: str) -> Dict:
        """Delete all files associated with an analysis ID"""

        deleted = []

        # Delete from uploads
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            upload_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(upload_path):
                os.remove(upload_path)
                deleted.append(upload_path)

        # Delete from results
        result_patterns = [
            f"{file_id}_analyzed.jpg",
            f"{file_id}_processed.jpg",
            f"{file_id}_thumb.jpg"
        ]

        for pattern in result_patterns:
            result_path = os.path.join(settings.RESULTS_DIR, pattern)
            if os.path.exists(result_path):
                os.remove(result_path)
                deleted.append(result_path)

        return {
            "file_id": file_id,
            "deleted_count": len(deleted),
            "deleted_paths": deleted
        }

    @staticmethod
    def list_all_files() -> Dict:
        """List all files in storage"""

        uploads = []
        results = []

        if os.path.exists(settings.UPLOAD_DIR):
            uploads = [
                {
                    "filename": f,
                    "size_bytes": os.path.getsize(os.path.join(settings.UPLOAD_DIR, f)),
                    "modified": datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(settings.UPLOAD_DIR, f))
                    ).isoformat()
                }
                for f in os.listdir(settings.UPLOAD_DIR)
                if os.path.isfile(os.path.join(settings.UPLOAD_DIR, f))
            ]

        if os.path.exists(settings.RESULTS_DIR):
            results = [
                {
                    "filename": f,
                    "size_bytes": os.path.getsize(os.path.join(settings.RESULTS_DIR, f)),
                    "modified": datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(settings.RESULTS_DIR, f))
                    ).isoformat()
                }
                for f in os.listdir(settings.RESULTS_DIR)
                if os.path.isfile(os.path.join(settings.RESULTS_DIR, f))
            ]

        return {
            "uploads": uploads,
            "results": results,
            "total_uploads": len(uploads),
            "total_results": len(results)
        }

    @staticmethod
    def clear_all_storage() -> Dict:
        """Clear all storage (use with caution!)"""

        deleted_count = 0

        for directory in [settings.UPLOAD_DIR, settings.RESULTS_DIR]:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                        deleted_count += 1

        return {
            "deleted_count": deleted_count,
            "message": "All storage cleared"
        }