#!/usr/bin/env python3
"""
QUICK FIXES SCRIPT - Fixes critical issues for hackathon demo
Run this before your presentation!
"""

import os
import sys
import re
from pathlib import Path

def fix_import_error():
    """Fix incomplete import in main_pipeline.py"""
    file_path = "main_pipeline.py"
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found!")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix incomplete import
    old_import = "from backend.reality_engine.sentiment_analyzer import"
    new_import = "from backend.reality_engine.sentiment_analyzer import AdvancedSentimentAnalyzer, SentimentResult"
    
    if old_import in content and "AdvancedSentimentAnalyzer" not in content.split(old_import)[0]:
        content = content.replace(old_import, new_import)
        print("✅ Fixed import error in main_pipeline.py")
    else:
        print("ℹ️ Import already fixed or not found")
        return True
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def add_data_loading_to_presentation():
    """Add real data loading to presentation_mode.py"""
    file_path = "presentation_mode.py"
    if not os.path.exists(file_path):
        print(f"❌ {file_path} not found!")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has real data loading
    if "pd.read_csv(\"data/processed/gap_analysis.csv\")" in content:
        print("ℹ️ Presentation mode already has data loading")
        return True
    
    # Find setup_data method and replace
    setup_data_pattern = r'def setup_data\(self\):.*?"""Load or create presentation data"""'
    
    new_setup_data = '''def setup_data(self):
        """Load or create presentation data"""
        # Try to load REAL data first
        try:
            gap_path = "data/processed/gap_analysis.csv"
            sentiment_path = "data/processed/sentiment_analysis.csv"
            
            if os.path.exists(gap_path) and os.path.exists(sentiment_path):
                gap_df = pd.read_csv(gap_path)
                sentiment_df = pd.read_csv(sentiment_path)
                
                # Use REAL products
                self.products = gap_df['product_name'].unique().tolist()
                if len(self.products) == 0:
                    raise ValueError("No products found")
                
                # Use REAL sentiment data
                self.sentiment_data = {}
                for _, row in gap_df.iterrows():
                    product = row['product_name']
                    self.sentiment_data[product] = {
                        "score": float(row.get('sentiment_score', 0.5)),
                        "trend": [float(row.get('sentiment_score', 0.5))] * 10,  # Simplified trend
                        "complaints": int(row.get('dissatisfaction_index', 0)),
                        "risk": str(row.get('risk_level', 'medium')).lower()
                    }
                
                # Generate REAL alerts from mismatches
                self.alerts = []
                for idx, (_, row) in enumerate(gap_df.iterrows(), 1):
                    if row.get('risk_level', '').lower() in ['high', 'critical']:
                        alert = {
                            "id": idx,
                            "product": row['product_name'],
                            "type": "Mis-selling Detected",
                            "severity": row.get('risk_level', 'medium').lower(),
                            "time": "Recently detected",
                            "description": f"Risk score: {row.get('overall_risk_score', 0):.2f}, Dissatisfaction: {row.get('dissatisfaction_index', 0):.1f}%"
                        }
                        self.alerts.append(alert)
                
                print("✅ Loaded REAL data from pipeline!")
                return
        except Exception as e:
            print(f"⚠️ Could not load real data: {e}, using sample data")
        
        # Fallback to sample data'''
    
    # Replace the method
    if 'def setup_data(self):' in content:
        # Find and replace the entire method
        lines = content.split('\n')
        new_lines = []
        in_method = False
        indent_level = 0
        
        for i, line in enumerate(lines):
            if 'def setup_data(self):' in line:
                in_method = True
                indent_level = len(line) - len(line.lstrip())
                # Add new method
                new_lines.append(new_setup_data)
                continue
            
            if in_method:
                current_indent = len(line) - len(line.lstrip()) if line.strip() else indent_level + 4
                if line.strip() and current_indent <= indent_level and 'def ' in line:
                    in_method = False
                    new_lines.append(line)
                elif not in_method:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Added real data loading to presentation_mode.py")
        return True
    else:
        print("⚠️ Could not find setup_data method to replace")
        return False

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        "data/mock/customer_reviews.csv",
        "data/mock/product_docs"
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("⚠️ Missing data files:")
        for f in missing:
            print(f"  - {f}")
        print("\n💡 Run: python mock_data_generator.py")
        return False
    
    print("✅ All required data files exist")
    return True

def verify_pipeline_outputs():
    """Check if pipeline has been run"""
    output_files = [
        "data/processed/extracted_promises.csv",
        "data/processed/sentiment_analysis.csv",
        "data/processed/gap_analysis.csv"
    ]
    
    missing = []
    for file_path in output_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("⚠️ Pipeline outputs missing:")
        for f in missing:
            print(f"  - {f}")
        print("\n💡 Run: python main_pipeline.py")
        return False
    
    print("✅ Pipeline outputs exist")
    return True

def main():
    """Run all quick fixes"""
    print("=" * 60)
    print("🔧 QUICK FIXES FOR HACKATHON DEMO")
    print("=" * 60)
    print()
    
    fixes_applied = 0
    
    # Fix 1: Import error
    print("1. Fixing import error...")
    if fix_import_error():
        fixes_applied += 1
    print()
    
    # Fix 2: Add data loading
    print("2. Adding real data loading to presentation...")
    if add_data_loading_to_presentation():
        fixes_applied += 1
    print()
    
    # Check 3: Data files
    print("3. Checking data files...")
    check_data_files()
    print()
    
    # Check 4: Pipeline outputs
    print("4. Checking pipeline outputs...")
    pipeline_run = verify_pipeline_outputs()
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Fixes applied: {fixes_applied}")
    
    if not pipeline_run:
        print("\n⚠️ IMPORTANT: Run the pipeline before demo:")
        print("   1. python mock_data_generator.py")
        print("   2. python main_pipeline.py")
        print("   3. streamlit run presentation_mode.py")
    else:
        print("\n✅ Ready for demo!")
        print("   Run: streamlit run presentation_mode.py")
    
    print()

if __name__ == "__main__":
    main()

