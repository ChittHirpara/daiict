# In veritas-finance/config.py
# Copy from STEP 3.3
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    # Paths
    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    MOCK_DATA_DIR = DATA_DIR / "mock"
    MODELS_DIR = BASE_DIR / "ml_models"
    
    # API Keys - ALL DISABLED FOR FREE OPERATION
    # Project uses FREE mock data by default
    # No API keys needed - everything works free!
    TWITTER_API_KEY = ""  # Empty = use free mock data
    REDDIT_CLIENT_ID = ""  # Empty = use free mock data
    NEWS_API_KEY = ""  # Empty = use free mock data
    
    # Force Free Mode - Ensures no paid services
    FORCE_FREE_MODE = True  # Always use free options
    
    # Model Settings
    SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    NER_MODEL = "en_core_web_sm"
    TOPIC_MODEL = "all-MiniLM-L6-v2"
    
    # Analysis Settings
    RISK_THRESHOLD = 0.7
    MIN_COMPLAINTS = 5
    
config = Config()