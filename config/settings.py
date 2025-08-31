import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    
    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./trading.db")
    
    # Financial Data Configuration
    DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "USD")
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", "300"))
    
    # AI Configuration
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration."""
        required_vars = []
        
        if not cls.OPENAI_API_KEY:
            required_vars.append("OPENAI_API_KEY")
        
        if required_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(required_vars)}")
        
        return True


# Development configuration
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = "DEBUG"


# Production configuration
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = "INFO"
    

# Configuration mapping
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def get_config():
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development")
    return config_map.get(env, DevelopmentConfig)
