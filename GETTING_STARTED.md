# AI-Powered Financial Trading Application

Your AI-powered financial trading application has been successfully created! 🎉

## Quick Start

### 1. Set up your environment variables
Copy the `.env.example` file to `.env` and add your API keys:
```bash
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY=your_openai_api_key_here`
- `ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here` (optional)

### 2. Start the application

**Windows:**
```bash
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

**Or manually:**
```bash
# Terminal 1 - Backend
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2 - Frontend  
streamlit run frontend/main.py --server.port 8501
```

### 3. Access the application
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Features

✅ **Stock Ticker Analysis**: Enter any stock ticker for AI-powered analysis
✅ **Currency Impact Assessment**: Analyze how currency situations affect trading decisions
✅ **AI Recommendations**: Get BUY/SELL/HOLD recommendations with confidence scores
✅ **Risk Assessment**: Comprehensive risk evaluation
✅ **Real-time Data**: Integration with Yahoo Finance and Alpha Vantage
✅ **Interactive Dashboard**: Beautiful Streamlit interface with charts
✅ **Technical Indicators**: P/E ratios, market cap analysis, and more

## Architecture

```
AlgoTradingGenAI/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── routers/         # API routes
│   └── services/        # Business logic
├── frontend/            # Streamlit frontend
│   ├── main.py         # Main UI
│   ├── components/     # UI components
│   └── utils/          # Frontend utilities
├── core/               # Shared business logic
│   ├── models/         # Data models
│   └── services/       # Core services
├── tests/              # Test suites
└── config/             # Configuration
```

## VS Code Tasks

Use Ctrl+Shift+P and search for "Tasks: Run Task":
- **Start Backend Server**: Launch the FastAPI backend
- **Start Frontend Server**: Launch the Streamlit frontend
- **Install Dependencies**: Install Python packages
- **Run Tests**: Execute test suite
- **Format Code**: Format code with Black
- **Lint Code**: Check code with Flake8

## API Endpoints

- `POST /api/v1/trading/analyze`: Analyze a stock ticker
- `GET /api/v1/trading/recommendations/{ticker}`: Get recommendations
- `POST /api/v1/trading/currency-impact`: Analyze currency impact
- `GET /api/v1/health/`: Health check

## Example Usage

1. **Enter a ticker** (e.g., AAPL, MSFT, GOOGL)
2. **Select analysis options** (currency, analysis type)
3. **Get AI recommendations** with confidence scores
4. **View currency impact** and risk assessment
5. **See technical indicators** and market sentiment

## Next Steps

1. **Add your API keys** to the `.env` file
2. **Customize the AI prompts** in `core/services/ai_analysis.py`
3. **Add more financial data sources** in `core/services/financial_data.py`
4. **Extend the UI** with more components in `frontend/components/`
5. **Add more sophisticated trading strategies**

## Troubleshooting

- **Backend not starting**: Check if port 8000 is available
- **Frontend not loading**: Ensure Streamlit dependencies are installed
- **API errors**: Verify your OpenAI API key in `.env`
- **No stock data**: Check internet connection and ticker symbols

Enjoy building your AI-powered trading application! 📈🤖
