import os
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from routes.auth_routes import router as auth_router
from routes.ai_routes import router as ai_router
from routes.chat_routes import router as chat_router
from routes.image_routes import router as image_router
from middleware.rate_limit_middleware import general_api_rate_limiter, limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Nonprofit Idea Coach API",
    description="Backend API for Nonprofit Idea Coach platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Global rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply general rate limiting to all API endpoints."""
    if request.url.path.startswith("/api/"):
        try:
            general_api_rate_limiter(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )
    
    response = await call_next(request)
    return response


# Root endpoint - redirect to web interface
@app.get("/")
async def root():
    """Redirect to the web interface."""
    return RedirectResponse(url="/static/index.html")

# API info endpoint
@app.get("/info")
async def api_info():
    """API information endpoint."""
    return {
        "message": "🚀 Nonprofit Idea Coach AI Assistant",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "web_interface": "/static/index.html",
            "docs": "/docs",
            "health": "/health",
            "api_info": "/api",
            "register": "/api/auth/register",
            "login": "/api/auth/login",
            "profile": "/api/auth/profile",
            "ai_generate": "/api/ai/generate",
            "ai_demo": "/api/ai/demo/generate",
            "content_types": "/api/ai/content-types",
            "chat": "/api/chat/message",
            "demo_chat": "/api/chat/demo",
            "generate_image": "/api/images/generate",
            "demo_image": "/api/images/demo",
            "image_types": "/api/images/types"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "OK",
        "timestamp": datetime.utcnow().isoformat()
    }


# API info endpoint
@app.get("/api")
async def api_info():
    """API information endpoint."""
    return {
        "message": "Nonprofit Idea Coach API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(image_router, prefix="/api")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )