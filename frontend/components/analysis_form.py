import streamlit as st
from typing import Dict, Any


def create_analysis_form() -> Dict[str, Any]:
    """Create the stock analysis form."""
    
    st.subheader("📈 Stock Analysis")
    
    with st.form("stock_analysis"):
        col1, col2 = st.columns(2)
        
        with col1:
            ticker = st.text_input(
                "Stock Ticker",
                placeholder="e.g., AAPL, MSFT",
                help="Enter a valid stock ticker symbol"
            )
            
            base_currency = st.selectbox(
                "Base Currency",
                ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD"],
                help="Select your base currency for analysis"
            )
        
        with col2:
            analysis_type = st.selectbox(
                "Analysis Type",
                ["comprehensive", "basic", "technical", "fundamental"],
                help="Select the type of analysis to perform"
            )
            
            include_currency = st.checkbox(
                "Include Currency Analysis",
                value=True,
                help="Include currency impact in the analysis"
            )
        
        submitted = st.form_submit_button(
            "🔍 Analyze Stock",
            use_container_width=True,
            type="primary"
        )
    
    if submitted:
        return {
            "ticker": ticker.upper().strip() if ticker else "",
            "base_currency": base_currency,
            "analysis_type": analysis_type,
            "include_currency_analysis": include_currency,
            "submitted": True
        }
    
    return {"submitted": False}


def create_quick_analysis_buttons():
    """Create quick analysis buttons for popular stocks."""
    
    st.subheader("⚡ Quick Analysis")
    st.write("Click to analyze popular stocks:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    popular_stocks = [
        ("AAPL", "Apple"),
        ("MSFT", "Microsoft"), 
        ("GOOGL", "Google"),
        ("TSLA", "Tesla"),
        ("AMZN", "Amazon"),
        ("NVDA", "NVIDIA"),
        ("META", "Meta"),
        ("NFLX", "Netflix")
    ]
    
    selected_ticker = None
    
    for i, (ticker, name) in enumerate(popular_stocks):
        col = [col1, col2, col3, col4][i % 4]
        
        with col:
            if st.button(f"{ticker}\n{name}", key=f"quick_{ticker}"):
                selected_ticker = ticker
    
    return selected_ticker
