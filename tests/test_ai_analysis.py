import pytest
from unittest.mock import Mock, patch
from core.services.ai_analysis import AIAnalysisService
from core.models.trading import StockData, TradingRecommendation, RecommendationType, RiskLevel


class TestAIAnalysisService:
    """Test cases for AIAnalysisService."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = AIAnalysisService("test_api_key")
    
    def create_sample_stock_data(self):
        """Create sample stock data for testing."""
        return StockData(
            ticker="AAPL",
            current_price=150.0,
            previous_close=148.5,
            currency="USD",
            pe_ratio=25.0
        )
    
    def create_sample_financials(self):
        """Create sample financial data for testing."""
        return {
            "market_cap": 2500000000000,
            "market_cap_category": "Mega Cap",
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "country": "United States",
            "profit_margin": 0.25,
            "debt_to_equity": 0.3,
            "return_on_equity": 0.8
        }
    
    def test_prepare_analysis_context(self):
        """Test preparation of analysis context."""
        stock_data = self.create_sample_stock_data()
        financials = self.create_sample_financials()
        
        context = self.service._prepare_analysis_context(stock_data, financials, None)
        
        assert context["ticker"] == "AAPL"
        assert context["current_price"] == 150.0
        assert context["price_change_percent"] == pytest.approx(1.01, abs=0.01)
        assert context["market_cap_category"] == "Mega Cap"
        assert context["sector"] == "Technology"
    
    def test_create_analysis_prompt(self):
        """Test creation of analysis prompt."""
        context = {
            "ticker": "AAPL",
            "current_price": 150.0,
            "previous_close": 148.5,
            "price_change_percent": 1.01,
            "currency": "USD",
            "market_cap_category": "Mega Cap",
            "sector": "Technology"
        }
        
        prompt = self.service._create_analysis_prompt(context)
        
        assert "AAPL" in prompt
        assert "$150.00" in prompt
        assert "Technology" in prompt
        assert "RECOMMENDATION:" in prompt
        assert "CONFIDENCE:" in prompt
    
    def test_parse_ai_recommendation(self):
        """Test parsing of AI recommendation response."""
        ai_response = """
        RECOMMENDATION: BUY
        CONFIDENCE: 0.85
        RISK_LEVEL: MEDIUM
        TARGET_PRICE: 160.00
        STOP_LOSS: 140.00
        REASONING: Strong fundamentals and positive market sentiment
        CURRENCY_IMPACT: Minimal impact due to USD operations
        """
        
        recommendation = self.service._parse_ai_recommendation(ai_response, "AAPL")
        
        assert recommendation.ticker == "AAPL"
        assert recommendation.recommendation == RecommendationType.BUY
        assert recommendation.confidence == 0.85
        assert recommendation.risk_level == RiskLevel.MEDIUM
        assert recommendation.target_price == 160.00
        assert recommendation.stop_loss == 140.00
        assert "Strong fundamentals" in recommendation.reasoning
        assert "Minimal impact" in recommendation.currency_impact
    
    @patch('openai.OpenAI')
    @pytest.mark.asyncio
    async def test_analyze_stock_for_trading_success(self, mock_openai):
        """Test successful stock analysis."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices[0].message.content = """
        RECOMMENDATION: BUY
        CONFIDENCE: 0.8
        RISK_LEVEL: LOW
        REASONING: Excellent financial performance
        """
        
        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        self.service.client = mock_client
        
        stock_data = self.create_sample_stock_data()
        financials = self.create_sample_financials()
        
        result = await self.service.analyze_stock_for_trading(stock_data, financials)
        
        assert isinstance(result, TradingRecommendation)
        assert result.ticker == "AAPL"
        assert result.recommendation == RecommendationType.BUY
        assert result.confidence == 0.8
    
    @patch('openai.OpenAI')
    @pytest.mark.asyncio
    async def test_analyze_stock_for_trading_error_handling(self, mock_openai):
        """Test error handling in stock analysis."""
        # Mock OpenAI to raise an exception
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        self.service.client = mock_client
        
        stock_data = self.create_sample_stock_data()
        financials = self.create_sample_financials()
        
        result = await self.service.analyze_stock_for_trading(stock_data, financials)
        
        # Should return fallback recommendation
        assert isinstance(result, TradingRecommendation)
        assert result.recommendation == RecommendationType.HOLD
        assert result.confidence == 0.5
        assert "AI analysis unavailable" in result.reasoning
