from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import setup_cors
from app.api.routes import upload, analysis, gallery
import os
from pathlib import Path

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered web application for detecting and analyzing image symmetry",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Setup CORS
setup_cors(app)

# Mount static file directories for uploads/results
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=settings.RESULTS_DIR), name="results")

# Include API routers BEFORE frontend routes
app.include_router(upload.router, prefix=settings.API_PREFIX)
app.include_router(analysis.router, prefix=settings.API_PREFIX)
app.include_router(gallery.router, prefix=settings.API_PREFIX)

# API-specific routes
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs",
        "endpoints": {
            "upload": f"{settings.API_PREFIX}/upload",
            "analyze": f"{settings.API_PREFIX}/analyze",
            "gallery": f"{settings.API_PREFIX}/gallery"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# Serve Next.js frontend
FRONTEND_BUILD_DIR = Path(__file__).parent.parent.parent / "frontend" / "out"

if FRONTEND_BUILD_DIR.exists():
    print(f"✅ Serving frontend from: {FRONTEND_BUILD_DIR}")
    
    # Mount Next.js static files
    app.mount("/_next", StaticFiles(directory=str(FRONTEND_BUILD_DIR / "_next")), name="next-static")
    
    # Catch-all route for SPA - must be last
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend files or index.html for SPA routing"""
        
        # Skip API routes
        if full_path.startswith("api/") or full_path.startswith("uploads/") or full_path.startswith("results/"):
            return {"error": "Not found"}, 404
        
        file_path = FRONTEND_BUILD_DIR / full_path
        
        # If specific file exists, serve it
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Check for .html extension
        html_path = FRONTEND_BUILD_DIR / f"{full_path}.html"
        if html_path.is_file():
            return FileResponse(html_path)
        
        # Default to index.html for SPA routing
        index_path = FRONTEND_BUILD_DIR / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        return {"error": "Frontend not found"}
else:
    print(f"⚠️  Frontend build directory not found: {FRONTEND_BUILD_DIR}")
    
    @app.get("/")
    async def root():
        return {
            "message": "Frontend not built yet",
            "api_docs": "/api/docs",
            "note": "Build the frontend with: cd frontend && npm run build"
        }


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"📁 Results directory: {settings.RESULTS_DIR}")
    print(f"🤖 Model path: {settings.MODEL_PATH}")
    print(f"🌐 Frontend directory: {FRONTEND_BUILD_DIR}")
    print(f"🌐 Frontend exists: {FRONTEND_BUILD_DIR.exists()}")
    print(f"✅ Application started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print(f"👋 {settings.APP_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=False
    )