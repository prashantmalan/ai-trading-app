# 🤖 AI-Powered Financial Trading Application

> A sophisticated trading recommendation system using FastAPI, Streamlit, and OpenAI GPT models

## 🎯 What It Does

- **AI Analysis**: Uses OpenAI GPT-3.5-turbo for intelligent stock analysis
- **Real-Time Data**: Fetches live market data via Yahoo Finance
- **Smart Recommendations**: Provides BUY/SELL/HOLD with confidence scores
- **Risk Assessment**: Categorizes investments as Low/Medium/High risk
- **Currency Analysis**: Multi-currency impact assessment
- **Plain English**: AI explanations accessible to non-financial users

## 🏗️ Architecture

```
Frontend (Streamlit) ←→ Backend (FastAPI) ←→ External APIs
     ↓                        ↓                  ↓
• Dashboard              • Trading API      • OpenAI
• Analysis Form          • Health Checks    • Yahoo Finance
• Results Display        • Documentation    • Alpha Vantage
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.8+, Pydantic, Uvicorn
- **Frontend**: Streamlit, Plotly, Pandas
- **AI**: OpenAI GPT-3.5-turbo
- **Data**: Yahoo Finance (yfinance), Alpha Vantage
- **Testing**: Pytest, comprehensive test suite

## ⚡ Quick Start

```bash
# Clone and setup
git clone https://github.com/prashantmalan/ai-trading-app.git
cd ai-trading-app
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your OpenAI API key to .env

# Run
python run_backend.py    # Terminal 1: Backend (port 8000)
python run_frontend.py   # Terminal 2: Frontend (port 8501)
```

## 📊 Example Output

```
🎯 RECOMMENDATION: BUY (85% Confidence)
💰 Target Price: $245.00
🛡️ Stop Loss: $215.00
⚠️ Risk Level: MEDIUM

📊 REASONING:
Company Performance: Apple shows strong fundamentals with healthy profit margins
Stock Price Situation: Currently trading below recent highs, good opportunity
Market Conditions: Technology sector showing positive momentum
Financial Health: Strong balance sheet with manageable debt levels
Currency Impact: Minimal risk as USD-based company
```

## 🎨 Key Features

### 🧠 AI-Powered Intelligence
- Advanced analysis considering technical indicators, fundamentals, market sentiment
- Confidence scoring (0-100%) for each recommendation
- Structured reasoning in plain English

### 📈 Comprehensive Data
- Real-time stock prices and market data
- Technical indicators: P/E ratios, market cap, debt-to-equity
- Currency analysis with exchange rate impact
- Historical context and trend analysis

### 🎯 Smart Output
- Clear BUY/SELL/HOLD recommendations
- AI-suggested target prices and stop-loss levels
- Risk categorization with detailed explanations
- Interactive charts and visualizations

## 📁 Project Structure

```
ai-trading-app/
├── backend/           # FastAPI application
│   ├── main.py       # App entry point
│   ├── routers/      # API endpoints
│   └── services/     # Business logic
├── frontend/         # Streamlit application
│   ├── main.py       # Frontend entry
│   ├── components/   # UI components
│   └── utils/        # API client
├── core/             # Shared business logic
│   ├── models/       # Data models
│   └── services/     # Core services
├── config/           # Configuration
├── tests/            # Test suite
└── screenshots/      # UI screenshots
```

## 🔄 API Endpoints

```
POST /api/v1/trading/analyze
- Analyzes stock and returns AI recommendations
- Input: {"ticker": "AAPL", "base_currency": "USD"}
- Output: Comprehensive analysis with recommendation

GET /api/v1/health
- Health check endpoint
- Returns: {"status": "healthy", "timestamp": "..."}
```

## 🧪 Core Services

### Financial Data Service
```python
async def get_stock_data(ticker: str) -> StockData:
    """Fetch real-time stock data from Yahoo Finance"""
    # Returns: price, volume, market cap, P/E ratio, etc.
```

### AI Analysis Service
```python
async def analyze_stock_for_trading(
    stock_data: StockData, 
    financials: Dict, 
    currency_analysis: Dict
) -> TradingRecommendation:
    """Generate AI-powered trading recommendation"""
    # Returns: BUY/SELL/HOLD with reasoning
```

### Currency Analysis Service
```python
async def analyze_currency_impact(
    ticker: str, 
    financials: Dict, 
    base_currency: str
) -> Dict:
    """Assess currency-related investment risks"""
    # Returns: risk level, exchange rate trends, hedging recommendations
```

## 🛡️ Security & Best Practices

- **API Key Protection**: Environment variables, no hardcoded secrets
- **Input Validation**: Pydantic models for all data validation
- **Error Handling**: Comprehensive error handling with fallback mechanisms
- **No Data Storage**: No persistent storage of user queries
- **Rate Limiting**: Respects external API limits

## 📊 Performance Features

- **Async Programming**: Non-blocking operations throughout
- **Intelligent Caching**: Data caching for improved performance
- **Fallback Systems**: Alternative recommendations when AI unavailable
- **Response Times**: < 5 seconds for most analyses

## 🔧 Development

```bash
# Run tests
python -m pytest

# Code formatting
black .
flake8 .

# Start with hot reload
uvicorn backend.main:app --reload --port 8000
streamlit run frontend/main.py --server.port 8501
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Architecture**: Detailed in ARCHITECTURE.md
- **Screenshots**: UI examples in SCREENSHOTS.md
- **Setup Guide**: Step-by-step in GETTING_STARTED.md

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

GNU Affero General Public License v3.0 - see LICENSE file

## 👨‍💻 Author

**Prashant Malan**
- Email: pragyan8519@gmail.com
- GitHub: [@prashantmalan](https://github.com/prashantmalan)
- Repository: [ai-trading-app](https://github.com/prashantmalan/ai-trading-app)

## ⚠️ Disclaimer

This application is for educational purposes only. Not financial advice. Always consult qualified financial professionals before making investment decisions.

---

**⭐ Star the repo if you find it helpful!**

**🔗 Try it:** https://github.com/prashantmalan/ai-trading-app
