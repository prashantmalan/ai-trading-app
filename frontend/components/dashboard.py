import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any


def create_dashboard():
    """Create the main trading dashboard."""
    
    st.header("📊 Trading Dashboard")
    
    # Portfolio overview (placeholder)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio Value", "$50,000", "2.3%")
    
    with col2:
        st.metric("Day's P&L", "+$1,250", "2.5%")
    
    with col3:
        st.metric("Active Positions", "5", "+1")
    
    with col4:
        st.metric("Win Rate", "68%", "3%")
    
    # Market overview chart
    st.subheader("Market Overview")
    
    # Sample market data
    market_data = {
        "Index": ["S&P 500", "NASDAQ", "DOW", "Russell 2000"],
        "Value": [4500, 14200, 35000, 2100],
        "Change": [1.2, 0.8, 0.5, -0.3]
    }
    
    fig = go.Figure(data=[
        go.Bar(
            x=market_data["Index"],
            y=market_data["Change"],
            marker_color=['green' if x > 0 else 'red' for x in market_data["Change"]]
        )
    ])
    
    fig.update_layout(
        title="Major Indices Performance (%)",
        xaxis_title="Index",
        yaxis_title="Change (%)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_watchlist():
    """Create a stock watchlist component."""
    
    st.subheader("📋 Watchlist")
    
    # Sample watchlist data
    watchlist = [
        {"Ticker": "AAPL", "Price": "$175.20", "Change": "+1.2%", "Alert": "🟢"},
        {"Ticker": "MSFT", "Price": "$380.50", "Change": "-0.5%", "Alert": "🟡"},
        {"Ticker": "GOOGL", "Price": "$140.80", "Change": "+2.1%", "Alert": "🟢"},
        {"Ticker": "TSLA", "Price": "$220.30", "Change": "-1.8%", "Alert": "🔴"},
    ]
    
    for stock in watchlist:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            st.write(f"**{stock['Ticker']}**")
        with col2:
            st.write(stock['Price'])
        with col3:
            color = "green" if "+" in stock['Change'] else "red"
            st.markdown(f"<span style='color: {color}'>{stock['Change']}</span>", unsafe_allow_html=True)
        with col4:
            st.write(stock['Alert'])


def create_recent_analysis():
    """Create recent analysis component."""
    
    st.subheader("🕒 Recent Analysis")
    
    recent_items = [
        {"Ticker": "NVDA", "Recommendation": "BUY", "Confidence": "85%", "Time": "2 min ago"},
        {"Ticker": "AMD", "Recommendation": "HOLD", "Confidence": "72%", "Time": "15 min ago"},
        {"Ticker": "INTC", "Recommendation": "SELL", "Confidence": "68%", "Time": "1 hour ago"},
    ]
    
    for item in recent_items:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
            
            with col1:
                st.write(f"**{item['Ticker']}**")
            with col2:
                rec_color = {"BUY": "green", "SELL": "red", "HOLD": "orange"}
                color = rec_color.get(item['Recommendation'], "gray")
                st.markdown(f"<span style='color: {color}'>{item['Recommendation']}</span>", unsafe_allow_html=True)
            with col3:
                st.write(item['Confidence'])
            with col4:
                st.write(item['Time'])
            
            st.divider()
