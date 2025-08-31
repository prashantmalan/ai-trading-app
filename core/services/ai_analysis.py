from typing import Dict, Any, Optional
import logging
from datetime import datetime
from openai import OpenAI
from ..models.trading import TradingRecommendation, RecommendationType, RiskLevel, StockData

logger = logging.getLogger(__name__)


class AIAnalysisService:
    """Service for AI-powered trading analysis and recommendations."""
    
    def __init__(self, openai_api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
    
    async def analyze_stock_for_trading(
        self, 
        stock_data: StockData, 
        company_financials: Dict[str, Any],
        currency_analysis: Optional[Dict[str, Any]] = None
    ) -> TradingRecommendation:
        """Generate AI-powered trading recommendation."""
        
        try:
            # Prepare context for AI analysis
            context = self._prepare_analysis_context(stock_data, company_financials, currency_analysis)
            
            # Generate recommendation using OpenAI
            prompt = self._create_analysis_prompt(context)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst providing trading recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            recommendation = self._parse_ai_recommendation(ai_response, stock_data.ticker)
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Error in AI analysis for {stock_data.ticker}: {e}")
            # Return a conservative fallback recommendation
            return TradingRecommendation(
                ticker=stock_data.ticker,
                recommendation=RecommendationType.HOLD,
                confidence=0.5,
                reasoning="AI analysis unavailable - conservative HOLD recommendation",
                risk_level=RiskLevel.MEDIUM
            )
    
    def _prepare_analysis_context(
        self, 
        stock_data: StockData, 
        financials: Dict[str, Any],
        currency_analysis: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Prepare comprehensive context for AI analysis."""
        
        price_change = ((stock_data.current_price - stock_data.previous_close) / stock_data.previous_close) * 100
        
        context = {
            'ticker': stock_data.ticker,
            'current_price': stock_data.current_price,
            'previous_close': stock_data.previous_close,
            'price_change_percent': round(price_change, 2),
            'currency': stock_data.currency,
            'market_cap': financials.get('market_cap'),
            'market_cap_category': financials.get('market_cap_category'),
            'pe_ratio': stock_data.pe_ratio or financials.get('pe_ratio'),
            'sector': financials.get('sector'),
            'industry': financials.get('industry'),
            'country': financials.get('country'),
            'profit_margin': financials.get('profit_margin'),
            'debt_to_equity': financials.get('debt_to_equity'),
            'return_on_equity': financials.get('return_on_equity'),
            'beta': financials.get('beta'),
            'dividend_yield': financials.get('dividend_yield'),
            '52_week_high': financials.get('52_week_high'),
            '52_week_low': financials.get('52_week_low'),
        }
        
        if currency_analysis:
            context['currency_analysis'] = currency_analysis
        
        return context
    
    def _create_analysis_prompt(self, context: Dict[str, Any]) -> str:
        """Create detailed prompt for AI analysis."""
        
        prompt = f"""
        Please analyze the following stock and provide a trading recommendation:

        STOCK INFORMATION:
        - Ticker: {context['ticker']}
        - Current Price: ${context['current_price']:.2f} ({context['currency']})
        - Previous Close: ${context['previous_close']:.2f}
        - Price Change: {context['price_change_percent']}%
        - Market Cap Category: {context['market_cap_category']}
        - Sector: {context['sector']}
        - Industry: {context['industry']}
        - Country: {context['country']}

        FINANCIAL METRICS:
        - P/E Ratio: {context.get('pe_ratio', 'N/A')}
        - Profit Margin: {context.get('profit_margin', 'N/A')}
        - Debt-to-Equity: {context.get('debt_to_equity', 'N/A')}
        - Return on Equity: {context.get('return_on_equity', 'N/A')}
        - Beta: {context.get('beta', 'N/A')}
        - Dividend Yield: {context.get('dividend_yield', 'N/A')}
        - 52 Week High: ${context.get('52_week_high', 'N/A')}
        - 52 Week Low: ${context.get('52_week_low', 'N/A')}

        CURRENCY ANALYSIS:
        {self._format_currency_analysis(context.get('currency_analysis'))}

        Please provide your analysis in the following format:
        RECOMMENDATION: [BUY/SELL/HOLD]
        CONFIDENCE: [0.0-1.0]
        RISK_LEVEL: [LOW/MEDIUM/HIGH]
        TARGET_PRICE: [price or N/A]
        STOP_LOSS: [price or N/A]
        REASONING: [detailed explanation of your recommendation considering all factors including currency impact]
        CURRENCY_IMPACT: [brief assessment of how currency situation affects the recommendation]
        """
        
        return prompt
    
    def _format_currency_analysis(self, currency_analysis: Optional[Dict[str, Any]]) -> str:
        """Format currency analysis for the prompt."""
        if not currency_analysis:
            return "No specific currency analysis provided."
        
        formatted = "Currency Impact Assessment:\n"
        for key, value in currency_analysis.items():
            formatted += f"- {key}: {value}\n"
        
        return formatted
    
    def _parse_ai_recommendation(self, ai_response: str, ticker: str) -> TradingRecommendation:
        """Parse AI response into structured recommendation."""
        
        lines = ai_response.strip().split('\n')
        
        # Default values
        recommendation = RecommendationType.HOLD
        confidence = 0.5
        risk_level = RiskLevel.MEDIUM
        target_price = None
        stop_loss = None
        reasoning = "AI analysis completed"
        currency_impact = None
        
        # Parse response
        for line in lines:
            line = line.strip()
            if line.startswith('RECOMMENDATION:'):
                rec_text = line.split(':', 1)[1].strip().upper()
                if rec_text in ['BUY', 'SELL', 'HOLD']:
                    recommendation = RecommendationType(rec_text)
            
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.split(':', 1)[1].strip())
                    confidence = max(0.0, min(1.0, confidence))  # Clamp between 0 and 1
                except ValueError:
                    pass
            
            elif line.startswith('RISK_LEVEL:'):
                risk_text = line.split(':', 1)[1].strip().upper()
                if risk_text in ['LOW', 'MEDIUM', 'HIGH']:
                    risk_level = RiskLevel(risk_text)
            
            elif line.startswith('TARGET_PRICE:'):
                try:
                    price_text = line.split(':', 1)[1].strip()
                    if price_text.replace('.', '').replace('$', '').isdigit():
                        target_price = float(price_text.replace('$', ''))
                except ValueError:
                    pass
            
            elif line.startswith('STOP_LOSS:'):
                try:
                    price_text = line.split(':', 1)[1].strip()
                    if price_text.replace('.', '').replace('$', '').isdigit():
                        stop_loss = float(price_text.replace('$', ''))
                except ValueError:
                    pass
            
            elif line.startswith('REASONING:'):
                reasoning = line.split(':', 1)[1].strip()
            
            elif line.startswith('CURRENCY_IMPACT:'):
                currency_impact = line.split(':', 1)[1].strip()
        
        return TradingRecommendation(
            ticker=ticker,
            recommendation=recommendation,
            confidence=confidence,
            reasoning=reasoning,
            risk_level=risk_level,
            target_price=target_price,
            stop_loss=stop_loss,
            currency_impact=currency_impact
        )
