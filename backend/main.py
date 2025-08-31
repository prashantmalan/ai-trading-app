from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from typing import Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.routers import trading, health
from backend.services.trading_service import TradingService
from core.services.financial_data import FinancialDataService
from core.services.ai_analysis import AIAnalysisService
from core.services.currency_analysis import CurrencyAnalysisService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global services
trading_service: Optional[TradingService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    global trading_service
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not found in environment variables")
    
    # Initialize services
    financial_service = FinancialDataService(alpha_vantage_key)
    ai_service = AIAnalysisService(openai_api_key) if openai_api_key else None
    currency_service = CurrencyAnalysisService(financial_service)
    
    trading_service = TradingService(financial_service, ai_service, currency_service)
    
    logger.info("Trading application started successfully")
    
    yield
    
    # Shutdown
    logger.info("Trading application shutting down")


# Create FastAPI app
app = FastAPI(
    title="AI-Powered Financial Trading API",
    description="API for AI-driven stock analysis and trading recommendations",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get trading service
def get_trading_service() -> TradingService:
    if trading_service is None:
        raise HTTPException(status_code=500, detail="Trading service not initialized")
    return trading_service


# Include routers with proper dependency injection
def get_trading_service_dependency():
    if trading_service is None:
        raise HTTPException(status_code=500, detail="Trading service not initialized")
    return trading_service

app.dependency_overrides[trading.get_trading_service] = get_trading_service_dependency

app.include_router(health.router, prefix="/api/v1")
app.include_router(trading.router, prefix="/api/v1")


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/")
async def root():
    return {
        "message": "AI-Powered Financial Trading API",
        "version": "1.0.0",
        "status": "running"
    }
