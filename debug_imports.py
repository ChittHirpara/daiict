
import sys
import os

print("Checking imports...")
try:
    from dotenv import load_dotenv
    print("✅ dotenv imported")
except ImportError as e:
    print(f"❌ dotenv failed: {e}")


# Gemini checks removed


try:
    from main_pipeline import VeritasFinancePipeline
    print("✅ VeritasFinancePipeline imported")
except ImportError as e:
    print(f"❌ VeritasFinancePipeline failed: {e}")
except Exception as e:
    print(f"❌ VeritasFinancePipeline runtime error: {e}")

print("Import check complete.")
