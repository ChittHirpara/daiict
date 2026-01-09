# In veritas-finance/setup.py
import os
import subprocess
import sys

def setup_project():
    print("🚀 Setting up Veritas Finance Project...")
    
    # 1. Create virtual environment
    print("1. Creating virtual environment...")
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # 2. Install requirements
    print("2. Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
    else:  # Mac/Linux
        pip_path = "venv/bin/pip"
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"])
    
    # 3. Download spaCy model
    print("3. Downloading spaCy model...")
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    
    # 4. Generate mock data
    print("4. Generating mock data...")
    subprocess.run([sys.executable, "mock_data_generator.py"])
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Activate virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate")
    print("\n2. Test the system:")
    print("   python backend/expectation_engine/promise_extractor.py")
    print("   python backend/reality_engine/sentiment_analyzer.py")

if __name__ == "__main__":
    setup_project()