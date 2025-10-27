from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import setup_cors
from app.api.routes import upload, analysis, gallery
import os


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

# Mount static file directories
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=settings.RESULTS_DIR), name="results")

# Include routers
app.include_router(upload.router, prefix=settings.API_PREFIX)
app.include_router(analysis.router, prefix=settings.API_PREFIX)
app.include_router(gallery.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint - API information"""
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


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting...")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")
    print(f"📁 Results directory: {settings.RESULTS_DIR}")
    print(f"🤖 Model path: {settings.MODEL_PATH}")
    print(f"✅ Application started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print(f"👋 {settings.APP_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    import os

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Must be 0.0.0.0 for Render
        port=int(os.environ.get("PORT", 8080)),  # Render sets PORT dynamically
        reload=False  # Turn off reload in production
    )
