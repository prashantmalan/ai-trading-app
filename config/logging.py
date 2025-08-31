import logging
from config.settings import get_config

def setup_logging():
    """Setup application logging."""
    
    config = get_config()
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('trading_app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Set specific loggers
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('streamlit').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)
