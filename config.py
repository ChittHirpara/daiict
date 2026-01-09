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
    
    # API Keys (for demo, use mock)
    TWITTER_API_KEY = "mock_twitter_key"
    REDDIT_CLIENT_ID = "mock_reddit_id"
    
    # Model Settings
    SENTIMENT_MODEL = "distilbert-base-uncased-finetuned-sst-2-english"
    NER_MODEL = "en_core_web_sm"
    TOPIC_MODEL = "all-MiniLM-L6-v2"
    
    # Analysis Settings
    RISK_THRESHOLD = 0.7
    MIN_COMPLAINTS = 5
    
config = Config()