#!/usr/bin/env python3
"""Quick test to verify dashboard setup"""

import sys
import os

print("=" * 60)
print("TESTING DASHBOARD SETUP")
print("=" * 60)

errors = []

# Test Python version
print(f"\n[OK] Python version: {sys.version.split()[0]}")

# Test imports
print("\nTesting imports...")
modules = {
    'streamlit': 'Streamlit',
    'pandas': 'Pandas',
    'plotly': 'Plotly',
    'numpy': 'NumPy',
    'PIL': 'Pillow',
    'fpdf': 'FPDF'
}

for module, name in modules.items():
    try:
        __import__(module)
        print(f"  [OK] {name}")
    except ImportError:
        print(f"  [ERROR] {name} - Run: pip install {module}")
        errors.append(module)

# Test backend imports
print("\nTesting backend imports...")
try:
    from backend.auth.auth_manager import AuthManager
    print("  [OK] AuthManager")
except ImportError as e:
    print(f"  [WARNING] AuthManager: {e}")

try:
    from backend.expectation_engine.promise_extractor import PromiseExtractor
    print("  [OK] PromiseExtractor")
except ImportError as e:
    print(f"  [WARNING] PromiseExtractor: {e}")

# Test data files
print("\nTesting data files...")
data_files = [
    "data/processed/extracted_promises.csv",
    "data/processed/sentiment_analysis.csv",
    "data/processed/gap_analysis.csv"
]

data_ok = True
for f in data_files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f"  [OK] {f} ({size} bytes)")
    else:
        print(f"  [ERROR] {f} - Run: python mock_data_generator.py then python main_pipeline.py")
        data_ok = False

# Summary
print("\n" + "=" * 60)
if errors:
    print("[ERROR] SETUP INCOMPLETE")
    print(f"\nMissing modules: {', '.join(errors)}")
    print("Run: pip install " + " ".join(errors))
elif not data_ok:
    print("[WARNING] SETUP PARTIAL - Missing data files")
    print("Run: python mock_data_generator.py")
    print("Then: python main_pipeline.py")
else:
    print("[OK] SETUP COMPLETE - Ready to run dashboard!")
    print("\nNext step: streamlit run dashboard.py")
print("=" * 60)
