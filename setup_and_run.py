#!/usr/bin/env python3
"""
Quick Setup and Run Script for VERITAS Dashboard
Fixes common issues and gets you running quickly!
"""

import subprocess
import sys
import os

def check_file_exists(filename):
    """Check if a file exists"""
    if not os.path.exists(filename):
        print(f"⚠️  Warning: {filename} not found")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("=" * 60)
    print("📦 STEP 1: Installing Dependencies")
    print("=" * 60)
    
    if not check_file_exists("requirements.txt"):
        print("⚠️  requirements.txt not found. Installing basic packages...")
        basic_packages = ["streamlit", "pandas", "plotly", "numpy", "pillow", "fpdf"]
        for package in basic_packages:
            try:
                print(f"   Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                print(f"   ⚠️  Could not install {package} automatically")
    else:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            print("   Try manually: pip install -r requirements.txt")
            return False
    
    return True

def generate_data():
    """Generate mock data if needed"""
    print("\n" + "=" * 60)
    print("📊 STEP 2: Generating Mock Data")
    print("=" * 60)
    
    if not check_file_exists("mock_data_generator.py"):
        print("⚠️  mock_data_generator.py not found. Skipping data generation.")
        return False
    
    try:
        subprocess.check_call([sys.executable, "mock_data_generator.py"])
        print("✅ Mock data generated successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Could not generate data: {e}")
        print("   Data might already exist or generator has issues.")
        return False

def run_pipeline():
    """Run the main pipeline"""
    print("\n" + "=" * 60)
    print("🔄 STEP 3: Running AI Pipeline")
    print("=" * 60)
    
    # Check if data files already exist
    data_files = [
        "data/processed/extracted_promises.csv",
        "data/processed/sentiment_analysis.csv",
        "data/processed/gap_analysis.csv"
    ]
    
    all_exist = all(os.path.exists(f) for f in data_files)
    
    if all_exist:
        print("✅ Data files already exist. Skipping pipeline.")
        return True
    
    if not check_file_exists("main_pipeline.py"):
        print("⚠️  main_pipeline.py not found. Skipping pipeline.")
        return False
    
    try:
        subprocess.check_call([sys.executable, "main_pipeline.py"])
        print("✅ Pipeline completed successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Pipeline error: {e}")
        print("   You can still try running the dashboard - it may work with existing data.")
        return False

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("\n" + "=" * 60)
    print("🚀 STEP 4: Launching Dashboard")
    print("=" * 60)
    
    if not check_file_exists("dashboard.py"):
        print("❌ dashboard.py not found!")
        return False
    
    print("✅ Starting Streamlit dashboard...")
    print("   Open your browser to: http://localhost:8501")
    print("   Press CTRL+C to stop\n")
    
    try:
        subprocess.check_call([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped by user.")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("\nTry manually: streamlit run dashboard.py")
        return False
    
    return True

def main():
    """Main setup and run sequence"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║        VERITAS FINANCE - Dashboard Setup & Run           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return
    
    # Run setup steps
    success = True
    success = install_dependencies() and success
    generate_data()  # Don't fail if this doesn't work
    run_pipeline()   # Don't fail if this doesn't work
    
    # Always try to launch dashboard
    if success:
        launch_dashboard()
    else:
        print("\n" + "=" * 60)
        print("⚠️  Setup had some issues, but trying dashboard anyway...")
        print("=" * 60)
        launch_dashboard()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n📋 Manual Setup Instructions:")
        print("   1. pip install -r requirements.txt")
        print("   2. python mock_data_generator.py")
        print("   3. python main_pipeline.py")
        print("   4. streamlit run dashboard.py")
