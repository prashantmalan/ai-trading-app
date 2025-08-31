from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
from .financial_data import FinancialDataService

logger = logging.getLogger(__name__)


class CurrencyAnalysisService:
    """Service for analyzing currency impact on trading decisions."""
    
    def __init__(self, financial_data_service: FinancialDataService):
        self.financial_data_service = financial_data_service
        self.major_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD', 'AUD']
    
    async def analyze_currency_impact(
        self, 
        ticker: str, 
        company_financials: Dict[str, Any],
        base_currency: str = 'USD'
    ) -> Dict[str, Any]:
        """Analyze how currency situation affects trading decision."""
        
        try:
            company_currency = company_financials.get('currency', 'USD')
            company_country = company_financials.get('country', 'Unknown')
            
            analysis = {
                'company_currency': company_currency,
                'base_currency': base_currency,
                'company_country': company_country,
                'currency_risk_level': 'LOW',
                'exchange_rate_trend': 'STABLE',
                'hedging_recommendation': 'NOT_REQUIRED',
                'impact_assessment': 'MINIMAL',
                'detailed_analysis': {}
            }
            
            # If currencies are the same, minimal impact
            if company_currency == base_currency:
                analysis['detailed_analysis']['same_currency'] = True
                analysis['impact_assessment'] = 'MINIMAL'
                return analysis
            
            # Get current exchange rate
            currency_data = await self.financial_data_service.get_currency_rate(
                company_currency, base_currency
            )
            
            if currency_data:
                analysis['current_exchange_rate'] = currency_data.exchange_rate
                analysis['detailed_analysis']['exchange_rate'] = currency_data.exchange_rate
            
            # Assess currency risk based on company location and business model
            risk_assessment = self._assess_currency_risk(company_financials, company_currency, base_currency)
            analysis.update(risk_assessment)
            
            # Analyze currency strength trends (simplified)
            trend_analysis = self._analyze_currency_trends(company_currency, base_currency)
            analysis.update(trend_analysis)
            
            # Generate recommendations
            recommendations = self._generate_currency_recommendations(analysis)
            analysis['recommendations'] = recommendations
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in currency analysis for {ticker}: {e}")
            return {
                'error': str(e),
                'currency_risk_level': 'UNKNOWN',
                'impact_assessment': 'UNCERTAIN'
            }
    
    def _assess_currency_risk(
        self, 
        financials: Dict[str, Any], 
        company_currency: str, 
        base_currency: str
    ) -> Dict[str, Any]:
        """Assess currency risk based on company characteristics."""
        
        risk_factors = []
        risk_level = 'LOW'
        
        # Check if company operates internationally
        sector = financials.get('sector', '').lower()
        industry = financials.get('industry', '').lower()
        
        # Higher risk sectors/industries
        international_sectors = [
            'technology', 'telecommunications', 'energy', 'materials', 
            'industrials', 'consumer discretionary'
        ]
        
        export_heavy_industries = [
            'semiconductors', 'software', 'oil & gas', 'mining',
            'automotive', 'aerospace', 'pharmaceuticals'
        ]
        
        if any(s in sector for s in international_sectors):
            risk_factors.append('International sector exposure')
            risk_level = 'MEDIUM'
        
        if any(i in industry for i in export_heavy_industries):
            risk_factors.append('Export-heavy industry')
            risk_level = 'MEDIUM'
        
        # Market cap consideration
        market_cap_category = financials.get('market_cap_category', '')
        if market_cap_category in ['Small Cap', 'Micro Cap']:
            risk_factors.append('Smaller company - higher currency sensitivity')
            risk_level = 'HIGH' if risk_level != 'LOW' else 'MEDIUM'
        
        # Emerging market currencies have higher volatility
        emerging_currencies = ['BRL', 'INR', 'RUB', 'ZAR', 'TRY', 'MXN']
        if company_currency in emerging_currencies or base_currency in emerging_currencies:
            risk_factors.append('Emerging market currency exposure')
            risk_level = 'HIGH'
        
        return {
            'currency_risk_level': risk_level,
            'risk_factors': risk_factors,
            'detailed_analysis': {
                'sector_risk': sector,
                'industry_risk': industry,
                'market_cap_impact': market_cap_category
            }
        }
    
    def _analyze_currency_trends(self, company_currency: str, base_currency: str) -> Dict[str, Any]:
        """Analyze currency strength trends (simplified analysis)."""
        
        # This is a simplified analysis - in production, you'd use historical data
        currency_strength = {
            'USD': 0.8,  # Strong
            'EUR': 0.6,  # Moderate
            'GBP': 0.5,  # Moderate
            'JPY': 0.3,  # Weaker
            'CHF': 0.9,  # Very Strong
            'CAD': 0.6,  # Moderate
            'AUD': 0.4,  # Weaker
        }
        
        company_strength = currency_strength.get(company_currency, 0.5)
        base_strength = currency_strength.get(base_currency, 0.5)
        
        if company_strength > base_strength + 0.2:
            trend = 'STRENGTHENING'
            impact = 'POSITIVE'
        elif company_strength < base_strength - 0.2:
            trend = 'WEAKENING'
            impact = 'NEGATIVE'
        else:
            trend = 'STABLE'
            impact = 'NEUTRAL'
        
        return {
            'exchange_rate_trend': trend,
            'trend_impact': impact,
            'detailed_analysis': {
                'company_currency_strength': company_strength,
                'base_currency_strength': base_strength,
                'relative_strength': company_strength - base_strength
            }
        }
    
    def _generate_currency_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate currency-related trading recommendations."""
        
        recommendations = []
        
        risk_level = analysis.get('currency_risk_level', 'LOW')
        trend = analysis.get('exchange_rate_trend', 'STABLE')
        trend_impact = analysis.get('trend_impact', 'NEUTRAL')
        
        if risk_level == 'HIGH':
            recommendations.append("Consider currency hedging due to high exposure")
            recommendations.append("Monitor exchange rate movements closely")
        
        if trend_impact == 'POSITIVE':
            recommendations.append("Favorable currency trends support the investment")
        elif trend_impact == 'NEGATIVE':
            recommendations.append("Unfavorable currency trends may impact returns")
        
        if trend == 'STRENGTHENING':
            recommendations.append("Company currency strengthening - positive for returns")
        elif trend == 'WEAKENING':
            recommendations.append("Company currency weakening - may reduce returns")
        
        if not recommendations:
            recommendations.append("Currency impact is minimal - focus on fundamentals")
        
        return recommendations
