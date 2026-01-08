#!/usr/bin/env python3
"""
Quick system test script for VERITAS Command Center
Tests all major components
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    required_packages = [
        'streamlit', 'fastapi', 'pandas', 'plotly', 
        'sqlalchemy', 'transformers', 'spacy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements_upgraded.txt")
        return False
    return True

def test_database():
    """Test database setup"""
    print("\n🔍 Testing database...")
    try:
        from database.db_manager import DatabaseManager
        from database.schema import Product
        
        db = DatabaseManager()
        
        # Try to get products
        products = db.get_all_products()
        print(f"  ✅ Database connected")
        print(f"  ✅ Found {len(products)} products")
        
        if len(products) == 0:
            print("  ⚠️  No products found. Run: python mock_data_generator.py")
            print("      Then: python main_pipeline_upgraded.py")
        
        db.close()
        return True
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        print("   Run: python setup_database.py")
        return False

def test_files():
    """Test if required files exist"""
    print("\n🔍 Testing files...")
    required_files = [
        'dashboard.py',
        'api/main.py',
        'main_pipeline_upgraded.py',
        'database/schema.py',
        'database/db_manager.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def test_api_structure():
    """Test API structure"""
    print("\n🔍 Testing API structure...")
    try:
        from api.main import app
        print("  ✅ FastAPI app created")
        
        # Check routes
        routes = [route.path for route in app.routes]
        key_routes = ['/api/v1/statistics', '/api/v1/products']
        
        for route in key_routes:
            if route in routes:
                print(f"  ✅ Route: {route}")
            else:
                print(f"  ⚠️  Route not found: {route}")
        
        return True
    except Exception as e:
        print(f"  ❌ API error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("  VERITAS Command Center - System Test")
    print("=" * 50)
    
    results = {
        'imports': test_imports(),
        'database': test_database(),
        'files': test_files(),
        'api': test_api_structure()
    }
    
    print("\n" + "=" * 50)
    print("  TEST RESULTS")
    print("=" * 50)
    
    all_passed = all(results.values())
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {test}")
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("  🎉 ALL TESTS PASSED!")
        print("  Your system is ready to launch!")
        print("\n  Next steps:")
        print("    1. Run: python api/main.py (Terminal 1)")
        print("    2. Run: streamlit run dashboard.py (Terminal 2)")
        print("  Or use: launch.bat (Windows)")
        return 0
    else:
        print("  ⚠️  SOME TESTS FAILED")
        print("  Please fix the issues above before launching")
        return 1

if __name__ == "__main__":
    sys.exit(main())
