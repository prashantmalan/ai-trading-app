import pytest
import asyncio
from core.services.financial_data import FinancialDataService
from core.models.trading import StockData


class TestFinancialDataService:
    """Test cases for FinancialDataService."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.service = FinancialDataService()
    
    @pytest.mark.asyncio
    async def test_get_stock_data_valid_ticker(self):
        """Test getting stock data for a valid ticker."""
        result = await self.service.get_stock_data("AAPL")
        
        assert result is not None
        assert isinstance(result, StockData)
        assert result.ticker == "AAPL"
        assert result.current_price > 0
        assert result.currency is not None
    
    @pytest.mark.asyncio
    async def test_get_stock_data_invalid_ticker(self):
        """Test getting stock data for an invalid ticker."""
        result = await self.service.get_stock_data("INVALIDTICKER123")
        
        # Should handle gracefully and return None
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_currency_rate(self):
        """Test getting currency exchange rate."""
        result = await self.service.get_currency_rate("USD", "EUR")
        
        assert result is not None
        assert result.base_currency == "USD"
        assert result.target_currency == "EUR"
        assert result.exchange_rate > 0
    
    @pytest.mark.asyncio
    async def test_get_currency_rate_same_currency(self):
        """Test getting currency rate for same currency."""
        result = await self.service.get_currency_rate("USD", "USD")
        
        assert result is not None
        assert result.exchange_rate == 1.0
    
    @pytest.mark.asyncio
    async def test_get_company_financials(self):
        """Test getting company financial data."""
        result = await self.service.get_company_financials("AAPL")
        
        assert isinstance(result, dict)
        assert "company_name" in result
        assert "sector" in result
        assert "currency" in result
        assert "market_cap_category" in result
