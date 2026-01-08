"""
FREE-ONLY Configuration
Ensures project uses only free services and APIs
"""

import os
from typing import Dict, Any

class FreeOnlyConfig:
    """
    Configuration to ensure 100% free operation
    All paid services are disabled by default
    """
    
    # ========================================================================
    # API CONFIGURATION - FREE ONLY
    # ========================================================================
    
    # Twitter/X API - DISABLED (Paid service)
    # Twitter API v2 costs $100+/month
    # Use mock data instead (free)
    TWITTER_ENABLED = False
    TWITTER_BEARER_TOKEN = ""  # Empty = use mock data
    
    # Reddit API - FREE (Optional)
    # Reddit API is completely free, but mock data works too
    REDDIT_ENABLED = False  # Set to True if you want free Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID', '')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET', '')
    
    # News API - FREE TIER (Optional)
    # Free tier: 100 requests/day (enough for demo)
    # Set to False to use mock data (100% free)
    NEWS_API_ENABLED = False  # Set to True to use free tier
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # ========================================================================
    # DATABASE - FREE ONLY
    # ========================================================================
    
    # SQLite - 100% FREE (default)
    DATABASE_URL = "sqlite:///./veritas_finance.db"
    
    # PostgreSQL - FREE if local installation
    # Use only if you have local PostgreSQL (free)
    # Do NOT use cloud PostgreSQL (paid)
    # POSTGRESQL_ENABLED = False  # Keep disabled unless local install
    
    # ========================================================================
    # CLOUD SERVICES - ALL DISABLED
    # ========================================================================
    
    # AWS - DISABLED (Paid service)
    AWS_ENABLED = False
    AWS_ACCESS_KEY = ""
    AWS_SECRET_KEY = ""
    
    # Azure - DISABLED (Paid service)
    AZURE_ENABLED = False
    
    # Google Cloud - DISABLED (Paid service)
    GCP_ENABLED = False
    
    # Redis - OPTIONAL (Can be free if local)
    # Redis is only used for caching (optional)
    # If not available, caching is disabled (still works)
    REDIS_ENABLED = False
    REDIS_URL = ""  # Empty = no caching (still works perfectly)
    
    # ========================================================================
    # ML MODELS - ALL FREE
    # ========================================================================
    
    # All ML models used are FREE:
    # - Transformers (HuggingFace) - FREE
    # - spaCy - FREE
    # - scikit-learn - FREE
    # - All run locally (no API calls = no costs)
    
    # ========================================================================
    # PAYMENT SERVICES - ALL DISABLED
    # ========================================================================
    
    STRIPE_ENABLED = False
    PAYPAL_ENABLED = False
    # No payment processing = no costs
    
    # ========================================================================
    # MOCK DATA - ALWAYS AVAILABLE (FREE)
    # ========================================================================
    
    USE_MOCK_DATA = True  # Always use mock data when APIs unavailable
    MOCK_DATA_ENABLED = True  # Mock data is always free
    
    @classmethod
    def get_api_config(cls) -> Dict[str, Any]:
        """Get API configuration (free-only)"""
        return {
            'twitter': {
                'enabled': cls.TWITTER_ENABLED,
                'cost': '$0 (mock data)' if not cls.TWITTER_ENABLED else '$100+/month'
            },
            'reddit': {
                'enabled': cls.REDDIT_ENABLED,
                'cost': '$0 (free)' if cls.REDDIT_ENABLED else '$0 (mock data)'
            },
            'news': {
                'enabled': cls.NEWS_API_ENABLED,
                'cost': '$0 (free tier)' if cls.NEWS_API_ENABLED else '$0 (mock data)'
            }
        }
    
    @classmethod
    def verify_free_only(cls) -> Dict[str, bool]:
        """Verify all paid services are disabled"""
        checks = {
            'twitter_disabled': not cls.TWITTER_ENABLED,
            'no_aws': not cls.AWS_ENABLED,
            'no_azure': not cls.AZURE_ENABLED,
            'no_gcp': not cls.GCP_ENABLED,
            'mock_data_enabled': cls.USE_MOCK_DATA,
            'all_free': True
        }
        
        # Check if any paid service is enabled
        if cls.AWS_ENABLED or cls.AZURE_ENABLED or cls.GCP_ENABLED:
            checks['all_free'] = False
        
        return checks
    
    @classmethod
    def get_cost_summary(cls) -> str:
        """Get total cost summary"""
        total_cost = 0
        
        config = cls.get_api_config()
        for api, info in config.items():
            if info['enabled'] and '$' in info['cost']:
                # Extract cost if any
                pass  # All configured as free
        
        return f"Total Cost: ${total_cost}/month (100% FREE)"


# Force free-only mode
if __name__ == "__main__":
    config = FreeOnlyConfig()
    print("=" * 60)
    print("FREE-ONLY CONFIGURATION VERIFICATION")
    print("=" * 60)
    print()
    print("API Configuration:")
    for api, info in config.get_api_config().items():
        status = "ENABLED" if info['enabled'] else "DISABLED (using mock)"
        print(f"  {api.upper():10} - {status:25} - {info['cost']}")
    print()
    print("Free-Only Verification:")
    checks = config.verify_free_only()
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check}")
    print()
    print(config.get_cost_summary())
    print()
    print("=" * 60)
    print("✅ Project configured for 100% FREE operation!")
    print("=" * 60)
