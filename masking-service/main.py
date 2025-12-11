"""
SADNxAI Masking Service
FastAPI service for data anonymization techniques
"""

import os
import sys

# Add parent directory to path for shared module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router

# Create FastAPI app
app = FastAPI(
    title="SADNxAI Masking Service",
    description="Data anonymization service supporting suppress, generalize, pseudonymize, and date-shift techniques",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize storage directories on startup"""
    storage_path = os.getenv("STORAGE_PATH", "/storage")
    directories = [
        os.path.join(storage_path, "input"),
        os.path.join(storage_path, "staging"),
        os.path.join(storage_path, "output"),
        os.path.join(storage_path, "reports"),
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print(f"Masking Service started. Storage path: {storage_path}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
