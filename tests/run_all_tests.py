#!/usr/bin/env python3
"""
Run all tests
"""
import unittest
import sys
import os
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_tests():
    """Discover and run all tests"""
    print("=" * 60)
    print("  VERITAS Command Center - Test Suite")
    print("=" * 60)
    print()
    
    # Test discovery
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Try to load each test file individually
    test_files = [
        'test_database',
        'test_ml_models',
        'test_integration',
        'test_api'  # May fail if FastAPI not available
    ]
    
    for test_file in test_files:
        try:
            tests = loader.loadTestsFromName(f'tests.{test_file}')
            suite.addTests(tests)
            print(f"[OK] Loaded: {test_file}")
        except Exception as e:
            print(f"[SKIP] Skipped: {test_file} - {e}")
    
    # Also try discovery
    try:
        discovered = loader.discover(
            os.path.dirname(__file__),
            pattern='test_*.py'
        )
        suite.addTests(discovered)
    except Exception as e:
        print(f"⚠️  Discovery warning: {e}")
    
    print()
    print("=" * 60)
    print("  Running Tests...")
    print("=" * 60)
    print()
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 60)
    print("  Test Results")
    print("=" * 60)
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print()
        print("  [SUCCESS] ALL TESTS PASSED!")
    else:
        print()
        print("  [WARNING] SOME TESTS FAILED")
        if result.failures:
            print("\n  Failures:")
            for test, traceback in result.failures:
                print(f"    - {test}")
        if result.errors:
            print("\n  Errors:")
            for test, traceback in result.errors:
                print(f"    - {test}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
