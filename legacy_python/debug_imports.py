
import sys
import os

print("Checking imports...")
try:
    from dotenv import load_dotenv
    print("✅ dotenv imported")
except ImportError as e:
    print(f"❌ dotenv failed: {e}")

<<<<<<< HEAD
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported")
except ImportError as e:
    print(f"❌ google.generativeai failed: {e}")

try:
    from backend.gemini_client import GeminiClient
    print("✅ GeminiClient imported")
    client = GeminiClient()
    if client.api_key:
         print("   API Key detected")
    else:
         print("   ⚠️ No API Key found in env")
except ImportError as e:
    print(f"❌ GeminiClient import failed: {e}")
except Exception as e:
    print(f"❌ GeminiClient init failed: {e}")
=======

# Gemini checks removed

>>>>>>> f52b126d82de756a540f1962a41d4d2955fbfa4e

try:
    from main_pipeline import VeritasFinancePipeline
    print("✅ VeritasFinancePipeline imported")
except ImportError as e:
    print(f"❌ VeritasFinancePipeline failed: {e}")
except Exception as e:
    print(f"❌ VeritasFinancePipeline runtime error: {e}")

print("Import check complete.")
