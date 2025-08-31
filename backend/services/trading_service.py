from typing import Optional
import logging
from core.services.financial_data import FinancialDataService
from core.services.ai_analysis import AIAnalysisService
from core.services.currency_analysis import CurrencyAnalysisService
from core.models.trading import AnalysisRequest, AnalysisResponse, StockData, TradingRecommendation

logger = logging.getLogger(__name__)


class TradingService:
    """Main service orchestrating trading analysis and recommendations."""
    
    def __init__(
        self,
        financial_service: FinancialDataService,
        ai_service: Optional[AIAnalysisService],
        currency_service: CurrencyAnalysisService
    ):
        self.financial_service = financial_service
        self.ai_service = ai_service
        self.currency_service = currency_service
    
    async def analyze_ticker(self, request: AnalysisRequest) -> AnalysisResponse:
        """Perform comprehensive ticker analysis."""
        
        try:
            logger.info(f"Starting analysis for ticker: {request.ticker}")
            
            # Fetch stock data
            stock_data = await self.financial_service.get_stock_data(request.ticker)
            if not stock_data:
                raise ValueError(f"Unable to fetch data for ticker: {request.ticker}")
            
            # Fetch company financials
            company_financials = await self.financial_service.get_company_financials(request.ticker)
            
            # Currency analysis
            currency_analysis = None
            if request.include_currency_analysis:
                currency_analysis = await self.currency_service.analyze_currency_impact(
                    request.ticker, company_financials, request.base_currency
                )
            
            # AI-powered recommendation
            recommendation = None
            if self.ai_service:
                recommendation = await self.ai_service.analyze_stock_for_trading(
                    stock_data, company_financials, currency_analysis
                )
            else:
                # Fallback recommendation logic
                recommendation = self._generate_fallback_recommendation(stock_data, company_financials)
            
            # Calculate technical indicators (simplified)
            technical_indicators = self._calculate_technical_indicators(stock_data, company_financials)
            
            # Determine market sentiment (simplified)
            market_sentiment = self._determine_market_sentiment(stock_data, company_financials)
            
            return AnalysisResponse(
                ticker=request.ticker,
                stock_data=stock_data,
                recommendation=recommendation,
                currency_analysis=currency_analysis,
                technical_indicators=technical_indicators,
                market_sentiment=market_sentiment
            )
            
        except Exception as e:
            logger.error(f"Error analyzing ticker {request.ticker}: {e}")
            raise
    
    def _generate_fallback_recommendation(self, stock_data: StockData, financials: dict) -> TradingRecommendation:
        """Generate a basic recommendation when AI service is unavailable."""
        from core.models.trading import RecommendationType, RiskLevel
        
        # Simple rule-based logic
        pe_ratio = stock_data.pe_ratio or financials.get('pe_ratio')
        price_change = ((stock_data.current_price - stock_data.previous_close) / stock_data.previous_close) * 100
        
        # Basic recommendation logic
        if pe_ratio and pe_ratio < 15 and price_change > -2:
            recommendation = RecommendationType.BUY
            confidence = 0.7
            reasoning = "Low P/E ratio and stable price suggests good value"
        elif pe_ratio and pe_ratio > 25 or price_change < -5:
            recommendation = RecommendationType.SELL
            confidence = 0.6
            reasoning = "High P/E ratio or significant price drop suggests caution"
        else:
            recommendation = RecommendationType.HOLD
            confidence = 0.5
            reasoning = "Mixed signals suggest holding current position"
        
        return TradingRecommendation(
            ticker=stock_data.ticker,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            risk_level=RiskLevel.MEDIUM
        )
    
    def _calculate_technical_indicators(self, stock_data: StockData, financials: dict) -> dict:
        """Calculate basic technical indicators."""
        
        indicators = {}
        
        # Price-based indicators
        price_change = ((stock_data.current_price - stock_data.previous_close) / stock_data.previous_close) * 100
        indicators['price_change_percent'] = round(price_change, 2)
        
        # Valuation indicators
        if stock_data.pe_ratio:
            indicators['pe_ratio'] = stock_data.pe_ratio
            indicators['pe_category'] = 'Low' if stock_data.pe_ratio < 15 else 'High' if stock_data.pe_ratio > 25 else 'Medium'
        
        # Market cap indicators
        market_cap = financials.get('market_cap')
        if market_cap:
            indicators['market_cap'] = market_cap
            indicators['market_cap_category'] = financials.get('market_cap_category', 'Unknown')
        
        # Financial health indicators
        debt_to_equity = financials.get('debt_to_equity')
        if debt_to_equity:
            indicators['debt_to_equity'] = debt_to_equity
            indicators['leverage_level'] = 'Low' if debt_to_equity < 0.3 else 'High' if debt_to_equity > 0.7 else 'Medium'
        
        return indicators
    
    def _determine_market_sentiment(self, stock_data: StockData, financials: dict) -> str:
        """Determine overall market sentiment for the stock."""
        
        price_change = ((stock_data.current_price - stock_data.previous_close) / stock_data.previous_close) * 100
        
        # Volume analysis (if available)
        volume = stock_data.volume
        avg_volume = financials.get('avg_volume')
        
        sentiment_score = 0
        
        # Price momentum
        if price_change > 2:
            sentiment_score += 2
        elif price_change > 0:
            sentiment_score += 1
        elif price_change < -2:
            sentiment_score -= 2
        elif price_change < 0:
            sentiment_score -= 1
        
        # Volume confirmation
        if volume and avg_volume and volume > avg_volume * 1.5:
            sentiment_score += 1 if price_change > 0 else -1
        
        # Financial health
        if financials.get('profit_margin', 0) > 0.1:
            sentiment_score += 1
        
        if financials.get('return_on_equity', 0) > 0.15:
            sentiment_score += 1
        
        # Determine sentiment
        if sentiment_score >= 3:
            return "Very Bullish"
        elif sentiment_score >= 1:
            return "Bullish"
        elif sentiment_score <= -3:
            return "Very Bearish"
        elif sentiment_score <= -1:
            return "Bearish"
        else:
            return "Neutral"
