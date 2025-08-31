import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
from typing import Dict, Any, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.dashboard import create_dashboard
from frontend.components.analysis_form import create_analysis_form
from frontend.components.results_display import display_results
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="AI-Powered Trading Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(45deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1e3c72;
        margin: 0.5rem 0;
    }
    
    .recommendation-buy {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .recommendation-sell {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .recommendation-hold {
        color: #ffc107;
        font-weight: bold;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">📈 AI-Powered Trading Assistant</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Initialize API client
    api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    api_client = APIClient(api_base_url)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API connection status
        if check_api_connection(api_client):
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.warning("Please ensure the backend server is running on port 8000")
        
        st.markdown("---")
        
        # Analysis settings
        st.subheader("Analysis Settings")
        base_currency = st.selectbox(
            "Base Currency",
            ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"],
            index=0
        )
        
        include_currency_analysis = st.checkbox("Include Currency Analysis", value=True)
        analysis_type = st.selectbox(
            "Analysis Type",
            ["comprehensive", "basic", "technical", "fundamental"],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This application uses AI to analyze stocks and provide trading recommendations 
        based on financial data and currency situation analysis.
        
        **Features:**
        - Real-time stock data
        - AI-powered recommendations
        - Currency impact analysis
        - Risk assessment
        - Technical indicators
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📊 Stock Analysis")
        
        # Analysis form
        with st.form("analysis_form"):
            ticker = st.text_input(
                "Enter Stock Ticker",
                placeholder="e.g., AAPL, MSFT, GOOGL",
                help="Enter a valid stock ticker symbol"
            ).upper()
            
            submitted = st.form_submit_button("🔍 Analyze Stock", use_container_width=True)
        
        if submitted and ticker:
            analyze_stock(
                ticker, 
                base_currency, 
                analysis_type, 
                include_currency_analysis, 
                api_client
            )
    
    with col2:
        if "analysis_result" in st.session_state:
            display_analysis_results(st.session_state.analysis_result)
        else:
            st.info("👈 Enter a stock ticker and click 'Analyze Stock' to get started!")
            
            # Sample dashboard
            st.subheader("📈 Sample Analysis")
            display_sample_dashboard()


def check_api_connection(api_client: APIClient) -> bool:
    """Check if API is accessible."""
    try:
        response = api_client.health_check()
        return response.get("status") == "healthy"
    except:
        return False


def analyze_stock(
    ticker: str, 
    base_currency: str, 
    analysis_type: str, 
    include_currency_analysis: bool,
    api_client: APIClient
):
    """Perform stock analysis."""
    
    if not ticker:
        st.error("Please enter a valid ticker symbol")
        return
    
    with st.spinner(f"🔄 Analyzing {ticker}..."):
        try:
            # Prepare request
            request_data = {
                "ticker": ticker,
                "base_currency": base_currency,
                "analysis_type": analysis_type,
                "include_currency_analysis": include_currency_analysis
            }
            
            # Make API call
            result = api_client.analyze_stock(request_data)
            
            if result:
                st.session_state.analysis_result = result
                st.success(f"✅ Analysis completed for {ticker}")
                st.rerun()
            else:
                st.error("Failed to analyze stock. Please check the ticker symbol.")
                
        except Exception as e:
            st.error(f"Error analyzing {ticker}: {str(e)}")


def display_analysis_results(result: Dict[str, Any]):
    """Display comprehensive analysis results."""
    
    st.subheader(f"📊 Analysis Results: {result['ticker']}")
    
    # Stock data
    stock_data = result.get('stock_data', {})
    recommendation = result.get('recommendation', {})
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_price = stock_data.get('current_price', 0)
        st.metric("Current Price", f"${current_price:.2f}")
    
    with col2:
        previous_close = stock_data.get('previous_close', 0)
        change = current_price - previous_close
        change_pct = (change / previous_close * 100) if previous_close else 0
        st.metric("Price Change", f"${change:.2f}", f"{change_pct:.2f}%")
    
    with col3:
        volume = stock_data.get('volume', 0)
        st.metric("Volume", f"{volume:,}" if volume else "N/A")
    
    with col4:
        market_cap = stock_data.get('market_cap')
        if market_cap:
            market_cap_formatted = f"${market_cap/1e9:.1f}B" if market_cap > 1e9 else f"${market_cap/1e6:.1f}M"
            st.metric("Market Cap", market_cap_formatted)
        else:
            st.metric("Market Cap", "N/A")
    
    st.markdown("---")
    
    # Recommendation
    rec_type = recommendation.get('recommendation', 'HOLD')
    confidence = recommendation.get('confidence', 0.5)
    risk_level = recommendation.get('risk_level', 'MEDIUM')
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🤖 AI Recommendation")
        
        # Color-coded recommendation
        if rec_type == 'BUY':
            st.markdown(f'<div class="recommendation-buy">🟢 {rec_type}</div>', unsafe_allow_html=True)
        elif rec_type == 'SELL':
            st.markdown(f'<div class="recommendation-sell">🔴 {rec_type}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="recommendation-hold">🟡 {rec_type}</div>', unsafe_allow_html=True)
        
        st.write(f"**Confidence:** {confidence:.1%}")
        st.write(f"**Risk Level:** {risk_level}")
        
        reasoning = recommendation.get('reasoning', '')
        if reasoning:
            st.write("**Reasoning:**")
            st.write(reasoning)
    
    with col2:
        # Confidence gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Confidence %"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Currency Analysis
    if result.get('currency_analysis'):
        st.markdown("---")
        st.subheader("💱 Currency Impact Analysis")
        display_currency_analysis(result['currency_analysis'])
    
    # Technical Indicators
    if result.get('technical_indicators'):
        st.markdown("---")
        st.subheader("📈 Technical Indicators")
        display_technical_indicators(result['technical_indicators'])
    
    # Market Sentiment
    if result.get('market_sentiment'):
        st.markdown("---")
        st.subheader("📊 Market Sentiment")
        sentiment = result['market_sentiment']
        st.write(f"**Overall Sentiment:** {sentiment}")


def display_currency_analysis(currency_analysis: Dict[str, Any]):
    """Display currency impact analysis."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Company Currency:** {currency_analysis.get('company_currency', 'N/A')}")
        st.write(f"**Base Currency:** {currency_analysis.get('base_currency', 'N/A')}")
        st.write(f"**Risk Level:** {currency_analysis.get('currency_risk_level', 'N/A')}")
        st.write(f"**Exchange Rate Trend:** {currency_analysis.get('exchange_rate_trend', 'N/A')}")
    
    with col2:
        recommendations = currency_analysis.get('recommendations', [])
        if recommendations:
            st.write("**Currency Recommendations:**")
            for rec in recommendations:
                st.write(f"• {rec}")


def display_technical_indicators(indicators: Dict[str, Any]):
    """Display technical indicators."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'pe_ratio' in indicators:
            st.metric("P/E Ratio", f"{indicators['pe_ratio']:.2f}")
        if 'price_change_percent' in indicators:
            st.metric("Price Change %", f"{indicators['price_change_percent']:.2f}%")
    
    with col2:
        if 'market_cap_category' in indicators:
            st.write(f"**Market Cap Category:** {indicators['market_cap_category']}")
        if 'leverage_level' in indicators:
            st.write(f"**Leverage Level:** {indicators['leverage_level']}")


def display_sample_dashboard():
    """Display a sample dashboard with placeholder data."""
    
    st.markdown("*This is a sample view. Analyze a stock to see real data.*")
    
    # Sample price chart
    import pandas as pd
    import numpy as np
    
    dates = pd.date_range('2024-01-01', periods=30, freq='D')
    prices = 150 + np.cumsum(np.random.randn(30) * 2)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name='Stock Price'))
    fig.update_layout(
        title="Sample Stock Price Chart",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
