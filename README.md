# AI-Powered Financial Trading Application

A sophisticated financial trading application that leverages generative AI to provide intelligent buy/sell recommendations based on stock ticker analysis and currency situation assessment.

## Features

- **Stock Ticker Analysis**: Real-time stock data retrieval and analysis
- **Currency Situation Assessment**: Multi-currency impact analysis for trading decisions
- **AI-Powered Recommendations**: Generative AI-driven buy/sell suggestions
- **Risk Assessment**: Comprehensive risk evaluation and portfolio management
- **Interactive Dashboard**: Real-time charts, metrics, and trading insights
- **Multi-API Integration**: Yahoo Finance, Alpha Vantage, and other financial data sources

## Architecture

### Backend (FastAPI)
- RESTful API endpoints for trading operations
- AI service integration with OpenAI/LangChain
- Financial data aggregation and processing
- Risk calculation and portfolio management

### Frontend (Streamlit)
- Interactive web interface
- Real-time data visualization
- Trading dashboard with charts and metrics
- User-friendly ticker input and recommendation display

### Core Services
- Financial data fetching and processing
- AI analysis and recommendation engine
- Currency conversion and impact analysis
- Risk assessment algorithms

## Installation

1. Clone the repository and navigate to the project directory
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Configuration

Create a `.env` file with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## Usage

### Running the Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running the Frontend
```bash
cd frontend
streamlit run main.py --server.port 8501
```

### API Endpoints
- `POST /api/v1/analyze`: Analyze a stock ticker
- `GET /api/v1/recommendations/{ticker}`: Get AI recommendations
- `POST /api/v1/currency-impact`: Assess currency situation
- `GET /api/v1/health`: Health check endpoint

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Formatting
```bash
black .
flake8 .
mypy .
```

### Project Structure
```
AlgoTradingGenAI/
├── backend/              # FastAPI backend
│   ├── main.py          # FastAPI application
│   ├── routers/         # API route handlers
│   ├── services/        # Business logic
│   └── models/          # Pydantic models
├── frontend/            # Streamlit frontend
│   ├── main.py         # Main Streamlit app
│   ├── components/     # UI components
│   └── utils/          # Frontend utilities
├── core/               # Shared business logic
│   ├── models/         # Data models
│   ├── services/       # Core services
│   └── utils/          # Utility functions
├── tests/              # Test suites
├── config/             # Configuration files
└── requirements.txt    # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
