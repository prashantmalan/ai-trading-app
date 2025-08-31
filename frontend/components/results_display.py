import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, Optional
from datetime import datetime


def display_results(analysis_result: Dict[str, Any]):
    """Display comprehensive analysis results."""
    
    if not analysis_result:
        st.error("No analysis results to display")
        return
    
    ticker = analysis_result.get('ticker', 'Unknown')
    st.header(f"📊 Analysis Results: {ticker}")
    
    # Display stock data
    display_stock_overview(analysis_result)
    
    # Display recommendation
    display_recommendation(analysis_result)
    
    # Display currency analysis if available
    if analysis_result.get('currency_analysis'):
        display_currency_analysis(analysis_result['currency_analysis'])
    
    # Display technical indicators
    if analysis_result.get('technical_indicators'):
        display_technical_indicators(analysis_result['technical_indicators'])
    
    # Display market sentiment
    if analysis_result.get('market_sentiment'):
        display_market_sentiment(analysis_result['market_sentiment'])


def display_stock_overview(result: Dict[str, Any]):
    """Display stock data overview."""
    
    stock_data = result.get('stock_data', {})
    
    st.subheader("📈 Stock Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        price = stock_data.get('current_price', 0)
        st.metric("Current Price", f"${price:.2f}")
    
    with col2:
        prev_close = stock_data.get('previous_close', 0)
        change = price - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        st.metric("Change", f"${change:.2f}", f"{change_pct:.2f}%")
    
    with col3:
        volume = stock_data.get('volume')
        if volume:
            volume_str = f"{volume:,}"
        else:
            volume_str = "N/A"
        st.metric("Volume", volume_str)
    
    with col4:
        currency = stock_data.get('currency', 'USD')
        st.metric("Currency", currency)


def display_recommendation(result: Dict[str, Any]):
    """Display AI recommendation."""
    
    recommendation = result.get('recommendation', {})
    
    st.subheader("🤖 AI Recommendation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        rec_type = recommendation.get('recommendation', 'HOLD')
        confidence = recommendation.get('confidence', 0.5)
        risk_level = recommendation.get('risk_level', 'MEDIUM')
        
        # Color-coded recommendation
        colors = {'BUY': 'green', 'SELL': 'red', 'HOLD': 'orange'}
        color = colors.get(rec_type, 'gray')
        
        st.markdown(f"### <span style='color: {color}'>{rec_type}</span>", unsafe_allow_html=True)
        st.write(f"**Confidence:** {confidence:.1%}")
        st.write(f"**Risk Level:** {risk_level}")
        
        reasoning = recommendation.get('reasoning', '')
        if reasoning:
            st.write("**Reasoning:**")
            st.write(reasoning)
        
        # Target price and stop loss
        target_price = recommendation.get('target_price')
        stop_loss = recommendation.get('stop_loss')
        
        if target_price:
            st.write(f"**Target Price:** ${target_price:.2f}")
        if stop_loss:
            st.write(f"**Stop Loss:** ${stop_loss:.2f}")
    
    with col2:
        # Confidence gauge
        create_confidence_gauge(confidence)


def create_confidence_gauge(confidence: float):
    """Create a confidence gauge chart."""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        title={'text': "Confidence %"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
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
    
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)


def display_currency_analysis(currency_analysis: Dict[str, Any]):
    """Display currency impact analysis."""
    
    st.subheader("💱 Currency Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Currency Information:**")
        st.write(f"Company Currency: {currency_analysis.get('company_currency', 'N/A')}")
        st.write(f"Base Currency: {currency_analysis.get('base_currency', 'N/A')}")
        st.write(f"Risk Level: {currency_analysis.get('currency_risk_level', 'N/A')}")
        st.write(f"Trend: {currency_analysis.get('exchange_rate_trend', 'N/A')}")
        
        if 'current_exchange_rate' in currency_analysis:
            rate = currency_analysis['current_exchange_rate']
            st.write(f"Exchange Rate: {rate:.4f}")
    
    with col2:
        recommendations = currency_analysis.get('recommendations', [])
        if recommendations:
            st.write("**Currency Recommendations:**")
            for rec in recommendations:
                st.write(f"• {rec}")


def display_technical_indicators(indicators: Dict[str, Any]):
    """Display technical indicators."""
    
    st.subheader("📊 Technical Indicators")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'pe_ratio' in indicators:
            pe_ratio = indicators['pe_ratio']
            pe_category = indicators.get('pe_category', '')
            st.metric("P/E Ratio", f"{pe_ratio:.2f}", pe_category)
        
        if 'price_change_percent' in indicators:
            change = indicators['price_change_percent']
            st.metric("Price Change %", f"{change:.2f}%")
    
    with col2:
        if 'market_cap_category' in indicators:
            market_cap_cat = indicators['market_cap_category']
            st.write(f"**Market Cap:** {market_cap_cat}")
        
        if 'leverage_level' in indicators:
            leverage = indicators['leverage_level']
            st.write(f"**Leverage:** {leverage}")
    
    with col3:
        if 'debt_to_equity' in indicators:
            debt_ratio = indicators['debt_to_equity']
            st.metric("Debt/Equity", f"{debt_ratio:.2f}")


def display_market_sentiment(sentiment: str):
    """Display market sentiment."""
    
    st.subheader("📈 Market Sentiment")
    
    sentiment_colors = {
        'Very Bullish': 'green',
        'Bullish': 'lightgreen',
        'Neutral': 'gray',
        'Bearish': 'orange',
        'Very Bearish': 'red'
    }
    
    color = sentiment_colors.get(sentiment, 'gray')
    st.markdown(f"### <span style='color: {color}'>{sentiment}</span>", unsafe_allow_html=True)


def display_error_message(error: str):
    """Display error message."""
    st.error(f"Analysis Error: {error}")
    st.info("Please check the ticker symbol and try again.")


def display_loading_message(ticker: str):
    """Display loading message."""
    st.info(f"🔄 Analyzing {ticker}... Please wait.")


def create_export_options(result: Dict[str, Any]):
    """Create export options for analysis results."""
    
    st.subheader("📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON", use_container_width=True):
            st.download_button(
                label="Download JSON",
                data=str(result),
                file_name=f"analysis_{result.get('ticker', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export Summary", use_container_width=True):
            summary = create_analysis_summary(result)
            st.download_button(
                label="Download Summary",
                data=summary,
                file_name=f"summary_{result.get('ticker', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )


def create_analysis_summary(result: Dict[str, Any]) -> str:
    """Create a text summary of analysis results."""
    
    ticker = result.get('ticker', 'Unknown')
    stock_data = result.get('stock_data', {})
    recommendation = result.get('recommendation', {})
    
    summary = f"""
STOCK ANALYSIS SUMMARY
======================
Ticker: {ticker}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STOCK DATA:
- Current Price: ${stock_data.get('current_price', 0):.2f}
- Previous Close: ${stock_data.get('previous_close', 0):.2f}
- Currency: {stock_data.get('currency', 'USD')}

RECOMMENDATION:
- Action: {recommendation.get('recommendation', 'N/A')}
- Confidence: {recommendation.get('confidence', 0):.1%}
- Risk Level: {recommendation.get('risk_level', 'N/A')}
- Reasoning: {recommendation.get('reasoning', 'N/A')}

MARKET SENTIMENT: {result.get('market_sentiment', 'N/A')}
"""
    
    return summary
