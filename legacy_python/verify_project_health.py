import sys
import os
import importlib.util
from pathlib import Path
import time
import subprocess

def check_file_exists(path):
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} Checking {path}...")
    return exists

def import_module(name, path=None):
    try:
        if path:
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[name] = module
            spec.loader.exec_module(module)
        else:
            importlib.import_module(name)
        print(f"✅ Import {name} successful")
        return True
    except Exception as e:
        print(f"❌ Import {name} failed: {e}")
        return False

def run_script(script_name):
    print(f"\n🔄 Running {script_name}...")
    try:
        result = subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        print(f"✅ {script_name} completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed. Error:\n{e.stderr}")
        return False

def main():
    print("🏥 STARTING PROJECT HEALTH CHECK\n")
    
    # 1. Check Data Directory Structure
    print("--- 1. Checking Directory Structure ---")
    data_dirs = ["data", "data/mock", "data/processed", "data/mock/product_docs"]
    for d in data_dirs:
        if not os.path.exists(d):
            print(f"⚠️ Directory {d} missing. Creating...")
            os.makedirs(d, exist_ok=True)
        else:
            print(f"✅ Directory {d} exists")

    # 2. Check Mock Data
    print("\n--- 2. Checking Mock Data ---")
    required_mock_files = [
        "data/mock/customer_reviews.csv",
        "data/mock/sentiment_time_series.csv"
    ]
    
    mock_files_exist = all(check_file_exists(f) for f in required_mock_files)
    
    if not mock_files_exist:
        print("⚠️ Missing mock data. Running mock_data_generator.py...")
        if run_script("mock_data_generator.py"):
            print("✅ Mock data generated.")
        else:
            print("❌ Failed to generate mock data. Aborting.")
            return

    # 3. Check Processed Data (Main Pipeline Output)
    print("\n--- 3. Checking Processed Data (Pipeline Output) ---")
    required_processed_files = [
        "data/processed/gap_analysis.csv",
        "data/processed/extracted_promises.csv",
        "data/processed/sentiment_analysis.csv"
    ]
    
    processed_files_exist = all(check_file_exists(f) for f in required_processed_files)
    
    if not processed_files_exist:
        print("⚠️ Missing processed data. Running main_pipeline.py...")
        print("(This may take a minute as it runs the NLP engines...)")
        if run_script("main_pipeline.py"):
            print("✅ Main pipeline executed successfully.")
        else:
            print("❌ Failed to run main pipeline. Dashboard may not show data.")
    
    # 4. Verify Backend Imports
    print("\n--- 4. Verifying Backend Modules ---")
    
    try:
        sys.path.append(os.getcwd())
        from backend.auth.auth_manager import AuthManager
        print("✅ AuthManager imported")
        auth = AuthManager()
        print(f"   Users loaded: {len(auth.get_users())}")
    except Exception as e:
        print(f"❌ AuthManager check failed: {e}")

    # 5. Dashboard Syntax Check
    print("\n--- 5. Verifying Dashboard Code ---")
    try:
        import py_compile
        py_compile.compile("dashboard.py", doraise=True)
        print("✅ dashboard.py syntax is valid")
    except Exception as e:
        print(f"❌ dashboard.py has syntax errors: {e}")

    print("\n-------------------------------------------")
    print("🎉 HEALTH CHECK COMPLETE")
    print("-------------------------------------------")
    print("To test the full project now:")
    print("1. Run: streamlit run dashboard.py")
    print("2. Login (or use default user if configured)")
    print("3. Navigate through ALL tabs on the sidebar")
    print("4. Verify data loads in Insights and Product Analysis")

if __name__ == "__main__":
    main()
