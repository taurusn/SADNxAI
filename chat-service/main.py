"""
SADNxAI Chat Service
Main orchestration service with LLM integration
"""

import os
import sys

# Service version - update this when deploying changes
SERVICE_VERSION = "1.1.0-ws"
BUILD_DATE = "2025-01-10"

# Add parent directory to path for shared module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.websocket import router as ws_router

# Create FastAPI app
app = FastAPI(
    title="SADNxAI Chat Service",
    description="Conversational AI service for data anonymization with Claude integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sadnxai.sadn.site",
        "https://internhub.sadn.site",
        "https://openings-necessarily-tower-para.trycloudflare.com",
        "https://screenshot-throw-markets-black.trycloudflare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routes
app.include_router(router)
app.include_router(ws_router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat-service"}


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    storage_path = os.getenv("STORAGE_PATH", "/storage")
    directories = [
        os.path.join(storage_path, "input"),
        os.path.join(storage_path, "staging"),
        os.path.join(storage_path, "output"),
        os.path.join(storage_path, "reports"),
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    print("=" * 60)
    print(f"  Chat Service v{SERVICE_VERSION} (built {BUILD_DATE})")
    print("=" * 60)
    print(f"  Storage path: {storage_path}")
    print(f"  Redis URL: {os.getenv('REDIS_URL', 'redis://localhost:6379/0')}")
    print(f"  Masking Service: {os.getenv('MASKING_SERVICE_URL', 'http://localhost:8001')}")
    print(f"  Validation Service: {os.getenv('VALIDATION_SERVICE_URL', 'http://localhost:8002')}")
    print(f"  LLM Mock Mode: {os.getenv('LLM_MOCK_MODE', 'false')}")
    print(f"  WebSocket: /api/ws/{{session_id}}")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
