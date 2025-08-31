from fastapi import APIRouter
from typing import Dict, Any
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI-Powered Financial Trading API",
        "version": "1.0.0"
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with service status."""
    
    status = {
        "status": "healthy",
        "service": "AI-Powered Financial Trading API",
        "version": "1.0.0",
        "components": {}
    }
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    status["components"]["openai"] = {
        "status": "configured" if openai_key else "missing",
        "required": True
    }
    
    status["components"]["alpha_vantage"] = {
        "status": "configured" if alpha_vantage_key else "missing",
        "required": False
    }
    
    # Overall status
    missing_required = any(
        comp["status"] == "missing" and comp["required"] 
        for comp in status["components"].values()
    )
    
    if missing_required:
        status["status"] = "degraded"
        status["message"] = "Some required components are not configured"
    
    return status
