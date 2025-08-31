from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging
from core.models.trading import AnalysisRequest, AnalysisResponse
from backend.services.trading_service import TradingService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/trading", tags=["trading"])


def get_trading_service() -> TradingService:
    """Dependency injection for trading service."""
    # This will be overridden by the main app dependency
    pass


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_ticker(
    request: AnalysisRequest,
    trading_service: TradingService = Depends(get_trading_service)
) -> AnalysisResponse:
    """
    Analyze a stock ticker and provide AI-powered trading recommendations.
    
    - **ticker**: Stock ticker symbol (e.g., AAPL, MSFT)
    - **base_currency**: Base currency for analysis (default: USD)
    - **analysis_type**: Type of analysis to perform (default: comprehensive)
    - **include_currency_analysis**: Whether to include currency impact analysis
    """
    try:
        logger.info(f"Received analysis request for ticker: {request.ticker}")
        
        if not request.ticker or len(request.ticker.strip()) == 0:
            raise HTTPException(status_code=400, detail="Ticker symbol is required")
        
        # Clean up ticker symbol
        request.ticker = request.ticker.strip().upper()
        
        # Perform analysis
        result = await trading_service.analyze_ticker(request)
        
        logger.info(f"Analysis completed for ticker: {request.ticker}")
        return result
        
    except ValueError as e:
        logger.error(f"Validation error for ticker {request.ticker}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error analyzing ticker {request.ticker}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")


@router.get("/recommendations/{ticker}")
async def get_recommendations(
    ticker: str,
    base_currency: str = "USD",
    trading_service: TradingService = Depends(get_trading_service)
) -> Dict[str, Any]:
    """
    Get trading recommendations for a specific ticker.
    
    - **ticker**: Stock ticker symbol
    - **base_currency**: Base currency for analysis
    """
    try:
        request = AnalysisRequest(
            ticker=ticker,
            base_currency=base_currency,
            analysis_type="recommendation",
            include_currency_analysis=True
        )
        
        result = await trading_service.analyze_ticker(request)
        
        return {
            "ticker": result.ticker,
            "recommendation": result.recommendation.dict(),
            "currency_analysis": result.currency_analysis,
            "market_sentiment": result.market_sentiment,
            "timestamp": result.recommendation.timestamp.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations for {ticker}: {e}")
        raise HTTPException(status_code=500, detail="Error generating recommendations")


@router.post("/currency-impact")
async def analyze_currency_impact(
    request: Dict[str, Any],
    trading_service: TradingService = Depends(get_trading_service)
) -> Dict[str, Any]:
    """
    Analyze currency impact for a specific ticker.
    
    Expected request format:
    {
        "ticker": "AAPL",
        "base_currency": "USD"
    }
    """
    try:
        ticker = request.get("ticker")
        base_currency = request.get("base_currency", "USD")
        
        if not ticker:
            raise HTTPException(status_code=400, detail="Ticker is required")
        
        analysis_request = AnalysisRequest(
            ticker=ticker,
            base_currency=base_currency,
            analysis_type="currency",
            include_currency_analysis=True
        )
        
        result = await trading_service.analyze_ticker(analysis_request)
        
        return {
            "ticker": ticker,
            "currency_analysis": result.currency_analysis,
            "company_currency": result.stock_data.currency,
            "base_currency": base_currency
        }
        
    except Exception as e:
        logger.error(f"Error in currency impact analysis: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing currency impact")
