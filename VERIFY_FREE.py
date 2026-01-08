#!/usr/bin/env python3
"""
Verify that project is configured for 100% free operation
"""
import os
import sys

def verify_free_config():
    """Verify all configurations are free"""
    print("=" * 70)
    print("  VERITAS Command Center - FREE VERIFICATION")
    print("=" * 70)
    print()
    
    issues = []
    warnings = []
    
    # Check API configurations
    print("1. API Configuration:")
    twitter_token = os.getenv('TWITTER_BEARER_TOKEN', '')
    reddit_id = os.getenv('REDDIT_CLIENT_ID', '')
    news_key = os.getenv('NEWS_API_KEY', '')
    
    if twitter_token:
        warnings.append("[WARNING] Twitter token found - Will use PAID API ($100+/month)")
        print("   [X] Twitter API token detected (PAID)")
    else:
        print("   [OK] Twitter: Using free mock data")
    
    if reddit_id:
        print("   [OK] Reddit: Using free API (cost: $0)")
    else:
        print("   [OK] Reddit: Using free mock data")
    
    if news_key:
        print("   [OK] News API: Using free tier (100 req/day, cost: $0)")
    else:
        print("   [OK] News API: Using free mock data")
    
    print()
    
    # Check database
    print("2. Database Configuration:")
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./veritas_finance.db')
    if 'sqlite' in db_url.lower():
        print("   [OK] Database: SQLite (FREE)")
    elif 'postgresql' in db_url.lower():
        if 'amazonaws.com' in db_url or 'azure' in db_url or 'gcp' in db_url:
            issues.append("[ERROR] Cloud database detected (PAID)")
            print("   [X] Database: Cloud PostgreSQL (PAID)")
        else:
            print("   [OK] Database: Local PostgreSQL (FREE)")
    else:
        print("   [OK] Database: SQLite (FREE)")
    
    print()
    
    # Check cloud services
    print("3. Cloud Services:")
    aws_key = os.getenv('AWS_ACCESS_KEY_ID', '')
    azure_key = os.getenv('AZURE_CLIENT_ID', '')
    gcp_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    
    if aws_key:
        issues.append("[ERROR] AWS credentials detected (PAID)")
        print("   [X] AWS: Credentials found (PAID)")
    else:
        print("   [OK] AWS: Not configured")
    
    if azure_key:
        issues.append("[ERROR] Azure credentials detected (PAID)")
        print("   [X] Azure: Credentials found (PAID)")
    else:
        print("   [OK] Azure: Not configured")
    
    if gcp_key:
        issues.append("[ERROR] GCP credentials detected (PAID)")
        print("   [X] GCP: Credentials found (PAID)")
    else:
        print("   [OK] GCP: Not configured")
    
    print()
    
    # Check Redis (optional)
    print("4. Optional Services:")
    redis_url = os.getenv('REDIS_URL', '')
    if redis_url:
        if 'redis.cloud' in redis_url or 'redislabs' in redis_url:
            warnings.append("[WARNING] Cloud Redis detected (may be PAID)")
            print("   [WARNING] Redis: Cloud Redis (may be PAID)")
        else:
            print("   [OK] Redis: Local Redis (FREE)")
    else:
        print("   [OK] Redis: Not configured (optional, caching disabled)")
    
    print()
    
    # Final summary
    print("=" * 70)
    print("  VERIFICATION SUMMARY")
    print("=" * 70)
    print()
    
    if issues:
        print("[ERROR] ISSUES FOUND (May incur costs):")
        for issue in issues:
            print(f"   {issue}")
        print()
        print("[ACTION REQUIRED] Remove paid service configurations")
        print()
        return False
    elif warnings:
        print("[WARNING] WARNINGS (May incur costs):")
        for warning in warnings:
            print(f"   {warning}")
        print()
        print("[RECOMMENDATION] Use free alternatives")
        print()
        return True
    else:
        print("[SUCCESS] ALL CHECKS PASSED!")
        print()
        print("[OK] No paid services detected")
        print("[OK] All APIs using free/mock data")
        print("[OK] Database is free (SQLite)")
        print("[OK] No cloud services configured")
        print()
        print("[COST] TOTAL COST: $0.00/month")
        print()
        print("[SUCCESS] Project is 100% FREE!")
        print()
        return True

if __name__ == "__main__":
    is_free = verify_free_config()
    sys.exit(0 if is_free else 1)
