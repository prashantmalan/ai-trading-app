from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from enum import Enum


class RecommendationType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class StockData(BaseModel):
    ticker: str
    current_price: float
    previous_close: float
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    pe_ratio: Optional[float] = None
    currency: str = "USD"
    timestamp: datetime = Field(default_factory=datetime.now)


class CurrencyData(BaseModel):
    base_currency: str
    target_currency: str
    exchange_rate: float
    timestamp: datetime = Field(default_factory=datetime.now)


class TradingRecommendation(BaseModel):
    ticker: str
    recommendation: RecommendationType
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    risk_level: RiskLevel
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    currency_impact: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class AnalysisRequest(BaseModel):
    ticker: str
    base_currency: str = "USD"
    analysis_type: str = "comprehensive"
    include_currency_analysis: bool = True


class AnalysisResponse(BaseModel):
    ticker: str
    stock_data: StockData
    recommendation: TradingRecommendation
    currency_analysis: Optional[Dict[str, Any]] = None
    technical_indicators: Optional[Dict[str, Union[float, str]]] = None
    market_sentiment: Optional[str] = None
