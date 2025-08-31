import yfinance as yf
import requests
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
import logging
from ..models.trading import StockData, CurrencyData

logger = logging.getLogger(__name__)


class FinancialDataService:
    """Service for fetching financial data from various sources."""
    
    def __init__(self, alpha_vantage_key: Optional[str] = None):
        self.alpha_vantage_key = alpha_vantage_key
        self.base_url = "https://www.alphavantage.co/query"
    
    async def get_stock_data(self, ticker: str) -> Optional[StockData]:
        """Fetch stock data for a given ticker."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1d")
            
            if hist.empty:
                logger.warning(f"No historical data found for {ticker}")
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            
            return StockData(
                ticker=ticker.upper(),
                current_price=float(current_price),
                previous_close=float(previous_close),
                market_cap=info.get('marketCap'),
                volume=int(hist['Volume'].iloc[-1]) if not hist['Volume'].empty else None,
                pe_ratio=info.get('trailingPE'),
                currency=info.get('currency', 'USD')
            )
        except Exception as e:
            logger.error(f"Error fetching stock data for {ticker}: {e}")
            return None
    
    async def get_currency_rate(self, from_currency: str, to_currency: str) -> Optional[CurrencyData]:
        """Fetch currency exchange rate."""
        try:
            if from_currency == to_currency:
                return CurrencyData(
                    base_currency=from_currency,
                    target_currency=to_currency,
                    exchange_rate=1.0
                )
            
            # Using Yahoo Finance for currency data
            pair = f"{from_currency}{to_currency}=X"
            currency_ticker = yf.Ticker(pair)
            hist = currency_ticker.history(period="1d")
            
            if hist.empty:
                logger.warning(f"No currency data found for {pair}")
                return None
            
            rate = hist['Close'].iloc[-1]
            
            return CurrencyData(
                base_currency=from_currency,
                target_currency=to_currency,
                exchange_rate=float(rate)
            )
        except Exception as e:
            logger.error(f"Error fetching currency rate {from_currency}/{to_currency}: {e}")
            return None
    
    async def get_company_financials(self, ticker: str) -> Dict[str, Any]:
        """Get comprehensive company financial data."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'company_name': info.get('longName', ticker),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'country': info.get('country'),
                'currency': info.get('currency', 'USD'),
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'revenue': info.get('totalRevenue'),
                'profit_margin': info.get('profitMargins'),
                'operating_margin': info.get('operatingMargins'),
                'return_on_equity': info.get('returnOnEquity'),
                'debt_to_equity': info.get('debtToEquity'),
                'current_ratio': info.get('currentRatio'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
                'avg_volume': info.get('averageVolume'),
                'market_cap_category': self._categorize_market_cap(info.get('marketCap')),
            }
        except Exception as e:
            logger.error(f"Error fetching company financials for {ticker}: {e}")
            return {}
    
    def _categorize_market_cap(self, market_cap: Optional[float]) -> str:
        """Categorize market cap size."""
        if not market_cap:
            return "Unknown"
        
        if market_cap >= 200_000_000_000:  # $200B+
            return "Mega Cap"
        elif market_cap >= 10_000_000_000:  # $10B+
            return "Large Cap"
        elif market_cap >= 2_000_000_000:   # $2B+
            return "Mid Cap"
        elif market_cap >= 300_000_000:     # $300M+
            return "Small Cap"
        else:
            return "Micro Cap"
