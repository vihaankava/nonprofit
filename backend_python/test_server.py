#!/usr/bin/env python3
"""
Simple test server to verify the authentication API is working.
Run this file to start the server on http://localhost:8000
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting Nonprofit Idea Coach Authentication API...")
    print("📖 API Documentation: http://localhost:8002/docs")
    print("🔍 Health Check: http://localhost:8002/health")
    print("🏠 Home: http://localhost:8002/")
    print("\n" + "="*50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8002,
        log_level="info"
    )