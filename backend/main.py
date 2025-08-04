from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api import auth, admin, user, health


def create_application() -> FastAPI:
    """Application factory to create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        debug=settings.DEBUG
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["authentication"])
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(user.router, prefix="/user", tags=["user"])
    app.include_router(health.router, tags=["health"])
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"{settings.PROJECT_NAME} is running",
            "version": settings.VERSION,
            "status": "healthy"
        }
    
    return app


# Create application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
