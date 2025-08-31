# 🏗️ System Architecture Documentation

## Overview

This document provides detailed technical architecture information for the AI-Powered Financial Trading Application. The system follows a modern microservices-inspired architecture with clear separation of concerns between frontend, backend, and core business logic.

## High-Level Architecture

### Architecture Principles

1. **Separation of Concerns**: Clear boundaries between UI, API, and business logic
2. **Dependency Injection**: Loose coupling through dependency injection patterns
3. **Async Programming**: Non-blocking operations for better performance
4. **Data Validation**: Strong typing and validation throughout the system
5. **Error Handling**: Comprehensive error handling and logging
6. **Testability**: Design for easy unit and integration testing

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Trading Application                        │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Port 8501)           Backend (Port 8000)            │
│  ┌─────────────────────┐      ┌─────────────────────────────┐   │
│  │   Streamlit App     │────▶ │      FastAPI Server         │   │
│  │                     │      │                             │   │
│  │ • Dashboard         │      │ • Trading Router            │   │
│  │ • Analysis Form     │      │ • Health Router             │   │
│  │ • Results Display   │      │ • Dependency Injection     │   │
│  │ • API Client        │      │ • Request Validation       │   │
│  └─────────────────────┘      └─────────────────────────────┘   │
│                                              │                  │
│                                              ▼                  │
│                               ┌─────────────────────────────┐   │
│                               │     Core Services Layer     │   │
│                               │                             │   │
│                               │ • Trading Service           │   │
│                               │ • AI Analysis Service       │   │
│                               │ • Financial Data Service    │   │
│                               │ • Currency Analysis Service │   │
│                               └─────────────────────────────┘   │
│                                              │                  │
│                                              ▼                  │
│                               ┌─────────────────────────────┐   │
│                               │    External API Layer       │   │
│                               │                             │   │
│                               │ • OpenAI API                │   │
│                               │ • Yahoo Finance API         │   │
│                               │ • Alpha Vantage API         │   │
│                               └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Component Architecture

### 1. Frontend Layer (Streamlit)

#### Main Application (`frontend/main.py`)
- **Purpose**: Entry point for the Streamlit application
- **Responsibilities**:
  - Application configuration and setup
  - Page routing and navigation
  - Session state management
  - Component orchestration

#### Dashboard Component (`frontend/components/dashboard.py`)
- **Purpose**: Main dashboard with key metrics and overview
- **Features**:
  - Market summary widgets
  - Recent analysis history
  - Performance metrics
  - Quick action buttons

#### Analysis Form Component (`frontend/components/analysis_form.py`)
- **Purpose**: User input form for stock analysis requests
- **Features**:
  - Stock ticker input with validation
  - Currency selection
  - Analysis options (technical, fundamental, etc.)
  - Form submission handling

#### Results Display Component (`frontend/components/results_display.py`)
- **Purpose**: Visualization of analysis results
- **Features**:
  - Recommendation cards
  - Interactive charts (Plotly)
  - Risk assessment visualization
  - Export functionality

#### API Client (`frontend/utils/api_client.py`)
- **Purpose**: Backend communication layer
- **Features**:
  - HTTP request handling
  - Error handling and retry logic
  - Response parsing
  - Authentication (if required)

### 2. Backend Layer (FastAPI)

#### Main Application (`backend/main.py`)
- **Purpose**: FastAPI application setup and configuration
- **Responsibilities**:
  - App initialization
  - Router registration
  - Middleware configuration
  - CORS setup
  - Dependency injection setup

#### Trading Router (`backend/routers/trading.py`)
- **Purpose**: Trading-related API endpoints
- **Endpoints**:
  - `POST /api/v1/trading/analyze`: Stock analysis
  - `GET /api/v1/trading/history`: Analysis history
  - `POST /api/v1/trading/compare`: Compare multiple stocks

#### Health Router (`backend/routers/health.py`)
- **Purpose**: Application health monitoring
- **Endpoints**:
  - `GET /api/v1/health`: Basic health check
  - `GET /api/v1/health/detailed`: Detailed system status

#### Trading Service (`backend/services/trading_service.py`)
- **Purpose**: Main orchestration service
- **Responsibilities**:
  - Coordinate multiple services
  - Data aggregation
  - Business logic enforcement
  - Error handling

### 3. Core Services Layer

#### AI Analysis Service (`core/services/ai_analysis.py`)

```python
class AIAnalysisService:
    """
    Handles AI-powered stock analysis using OpenAI's GPT models.
    """
    
    async def analyze_stock_for_trading(
        self, 
        stock_data: StockData, 
        financials: Dict[str, Any],
        currency_analysis: Optional[Dict[str, Any]] = None
    ) -> TradingRecommendation:
        """
        Main analysis method that:
        1. Prepares comprehensive context
        2. Creates structured AI prompt
        3. Calls OpenAI API
        4. Parses and validates response
        5. Returns structured recommendation
        """
```

**Key Features**:
- **Context Preparation**: Aggregates all relevant data
- **Prompt Engineering**: Structured prompts for consistent results
- **Response Parsing**: Reliable extraction of recommendations
- **Error Handling**: Fallback recommendations when AI unavailable

#### Financial Data Service (`core/services/financial_data.py`)

```python
class FinancialDataService:
    """
    Handles retrieval and processing of financial market data.
    """
    
    async def get_stock_data(self, ticker: str) -> StockData:
        """
        Fetches comprehensive stock data including:
        - Current price and volume
        - Market cap and financial ratios
        - Historical performance
        - Company fundamentals
        """
    
    async def get_company_financials(self, ticker: str) -> Dict[str, Any]:
        """
        Retrieves detailed company financial information:
        - Income statement metrics
        - Balance sheet data
        - Cash flow information
        - Valuation ratios
        """
```

**Key Features**:
- **Multi-Source Data**: Yahoo Finance primary, Alpha Vantage backup
- **Data Validation**: Ensures data quality and completeness
- **Caching**: Implements intelligent caching for performance
- **Rate Limiting**: Respects API limits

#### Currency Analysis Service (`core/services/currency_analysis.py`)

```python
class CurrencyAnalysisService:
    """
    Analyzes currency impact on investment decisions.
    """
    
    async def analyze_currency_impact(
        self,
        ticker: str,
        company_financials: Dict[str, Any],
        base_currency: str = "USD"
    ) -> Dict[str, Any]:
        """
        Assesses currency-related investment risks:
        - Exchange rate trends
        - Currency exposure analysis
        - Hedging recommendations
        - Risk level assessment
        """
```

### 4. Data Models Layer

#### Trading Models (`core/models/trading.py`)

```python
# Request/Response Models
class AnalysisRequest(BaseModel):
    ticker: str
    base_currency: str = "USD"
    analysis_type: str = "comprehensive"
    include_currency_analysis: bool = True

class AnalysisResponse(BaseModel):
    ticker: str
    stock_data: StockData
    recommendation: TradingRecommendation
    currency_analysis: Optional[Dict[str, Any]] = None
    technical_indicators: Optional[Dict[str, Union[float, str]]] = None
    market_sentiment: Optional[str] = None

# Core Business Models
class StockData(BaseModel):
    ticker: str
    current_price: float
    previous_close: float
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    pe_ratio: Optional[float] = None
    currency: str = "USD"
    timestamp: datetime = Field(default_factory=datetime.now)

class TradingRecommendation(BaseModel):
    ticker: str
    recommendation: RecommendationType  # BUY/SELL/HOLD
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    risk_level: RiskLevel  # LOW/MEDIUM/HIGH
    target_price: Optional[float] = None
    stop_loss: Optional[float] = None
    currency_impact: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
```

## Data Flow Architecture

### Request Processing Flow

```
┌─────────────────┐
│   User Input    │
│   (Frontend)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Form Validation│
│  & Submission   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   API Request   │
│  (HTTP POST)    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  FastAPI Router │
│  (Validation)   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Trading Service │
│ (Orchestration) │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Financial Data  │    │ Currency        │    │ Company         │
│ Service         │    │ Analysis        │    │ Fundamentals    │
│ (Yahoo Finance) │    │ Service         │    │ (Market Data)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────┬───────────┴──────────┬───────────┘
                     │                      │
                     ▼                      ▼
           ┌─────────────────┐    ┌─────────────────┐
           │   Data          │    │   Context       │
           │   Aggregation   │    │   Preparation   │
           └─────────┬───────┘    └─────────┬───────┘
                     │                      │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌─────────────────┐
                     │  AI Analysis    │
                     │  Service        │
                     │  (OpenAI API)   │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  Response       │
                     │  Parsing &      │
                     │  Validation     │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  Trading        │
                     │  Recommendation │
                     │  Generation     │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  API Response   │
                     │  (JSON)         │
                     └─────────┬───────┘
                               │
                               ▼
                     ┌─────────────────┐
                     │  Frontend       │
                     │  Display        │
                     │  (Charts & UI)  │
                     └─────────────────┘
```

### AI Analysis Pipeline

```
┌─────────────────┐
│  Market Data    │
│  Collection     │
├─────────────────┤
│ • Stock Price   │
│ • Volume        │
│ • Market Cap    │
│ • P/E Ratio     │
│ • 52W High/Low  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Financial      │
│  Fundamentals   │
├─────────────────┤
│ • Profit Margin │
│ • Debt/Equity   │
│ • ROE           │
│ • Beta          │
│ • Sector Info   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Currency       │
│  Analysis       │
├─────────────────┤
│ • Exchange Rate │
│ • Trend Analysis│
│ • Risk Level    │
│ • Hedging Rec.  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Context        │
│  Preparation    │
├─────────────────┤
│ • Data Norm.    │
│ • Template Fill │
│ • Validation    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  AI Prompt      │
│  Engineering    │
├─────────────────┤
│ • Structured    │
│ • Comprehensive │
│ • Consistent    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  OpenAI API     │
│  Call           │
├─────────────────┤
│ • GPT-3.5-turbo │
│ • Temperature   │
│ • Max Tokens    │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Response       │
│  Parsing        │
├─────────────────┤
│ • Recommendation│
│ • Confidence    │
│ • Risk Level    │
│ • Reasoning     │
│ • Target Price  │
│ • Stop Loss     │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Validation &   │
│  Formatting     │
├─────────────────┤
│ • Type Checking │
│ • Range Validation │
│ • Error Handling │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│  Trading        │
│  Recommendation │
│  Output         │
└─────────────────┘
```

## Configuration Management

### Environment Variables

```python
# Core Configuration
OPENAI_API_KEY=sk-...           # OpenAI API key for AI analysis
ALPHA_VANTAGE_API_KEY=...       # Alpha Vantage API key (optional)
ENVIRONMENT=development         # Environment (development/production)
LOG_LEVEL=INFO                 # Logging level
DEBUG=True                     # Debug mode

# API Configuration
API_HOST=0.0.0.0              # API server host
API_PORT=8000                 # API server port
FRONTEND_PORT=8501            # Frontend server port

# AI Configuration
AI_MODEL=gpt-3.5-turbo        # OpenAI model to use
MAX_TOKENS=1000               # Maximum tokens per request
TEMPERATURE=0.7               # AI response randomness

# Financial Data Configuration
DEFAULT_CURRENCY=USD          # Default base currency
CACHE_TIMEOUT=300            # Data cache timeout (seconds)
```

### Settings Management (`config/settings.py`)

```python
class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Core settings
    openai_api_key: str
    alpha_vantage_api_key: Optional[str] = None
    environment: str = "development"
    debug: bool = False
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_port: int = 8501
    
    # AI settings
    ai_model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

## Error Handling Strategy

### Error Categories

1. **Validation Errors**: Invalid input data
2. **External API Errors**: Third-party service failures
3. **AI Analysis Errors**: OpenAI API issues
4. **System Errors**: Internal application errors

### Error Handling Flow

```python
try:
    # Main business logic
    result = await trading_service.analyze_stock(request)
    return result
except ValidationError as e:
    # Return 422 with validation details
    raise HTTPException(status_code=422, detail=str(e))
except ExternalAPIError as e:
    # Return 502 with service unavailable message
    raise HTTPException(status_code=502, detail="External service unavailable")
except AIAnalysisError as e:
    # Return fallback recommendation
    return generate_fallback_recommendation(request.ticker)
except Exception as e:
    # Log error and return 500
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

## Security Considerations

### API Key Management
- Environment variables for sensitive data
- No hardcoded secrets in code
- Separate keys for development/production

### Input Validation
- Pydantic models for request validation
- Stock ticker format validation
- SQL injection prevention (no direct DB queries)

### Rate Limiting
- Respect external API rate limits
- Implement request throttling if needed
- Graceful degradation under load

### CORS Configuration
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Performance Optimizations

### Caching Strategy
- In-memory caching for frequently accessed data
- TTL-based cache expiration
- Cache invalidation on data updates

### Async Programming
- Non-blocking I/O operations
- Concurrent API calls where possible
- Async/await throughout the stack

### Connection Pooling
- HTTP client connection reuse
- Database connection pooling (if using DB)
- Resource management

## Monitoring and Logging

### Logging Configuration (`config/logging.py`)
```python
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}
```

### Health Monitoring
- Application health endpoints
- External dependency health checks
- Performance metrics collection

## Testing Strategy

### Test Categories
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Service interaction testing
3. **End-to-End Tests**: Full workflow testing
4. **Performance Tests**: Load and stress testing

### Test Structure
```
tests/
├── unit/
│   ├── test_ai_analysis.py
│   ├── test_financial_data.py
│   └── test_currency_analysis.py
├── integration/
│   ├── test_trading_service.py
│   └── test_api_endpoints.py
└── e2e/
    └── test_full_workflow.py
```

## Deployment Architecture

### Local Development
```
Frontend (localhost:8501) ←→ Backend (localhost:8000) ←→ External APIs
```

### Production Deployment (Future)
```
Load Balancer ←→ Frontend Instances ←→ Backend Instances ←→ External APIs
                     ↓                        ↓
               Static Assets             Application Logs
                  (CDN)                  (Centralized)
```

## Scalability Considerations

### Horizontal Scaling
- Stateless service design
- Load balancer compatibility
- Database connection management

### Vertical Scaling
- Resource monitoring
- Performance bottleneck identification
- Memory and CPU optimization

### Caching Layers
- Application-level caching
- Redis for distributed caching (future)
- CDN for static assets (future)

This architecture provides a solid foundation for a production-ready AI trading application with clear separation of concerns, comprehensive error handling, and scalability considerations.
