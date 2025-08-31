import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """Client for communicating with the FastAPI backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/health/")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
    
    def analyze_stock(self, request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Analyze a stock ticker."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/trading/analyze",
                json=request_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_detail = e.response.json().get('detail', 'Bad request')
                logger.error(f"Bad request: {error_detail}")
                raise ValueError(error_detail)
            else:
                logger.error(f"HTTP error during analysis: {e}")
                raise
        except Exception as e:
            logger.error(f"Error analyzing stock: {e}")
            raise
    
    def get_recommendations(self, ticker: str, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        """Get trading recommendations for a ticker."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/trading/recommendations/{ticker}",
                params={"base_currency": base_currency}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return None
    
    def analyze_currency_impact(self, ticker: str, base_currency: str = "USD") -> Optional[Dict[str, Any]]:
        """Analyze currency impact for a ticker."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/trading/currency-impact",
                json={"ticker": ticker, "base_currency": base_currency}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error analyzing currency impact: {e}")
            return None
