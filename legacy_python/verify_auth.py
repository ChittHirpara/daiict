# verify_auth.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from backend.auth.auth_manager import AuthManager

def test_auth():
    print("Initializing AuthManager...")
    auth = AuthManager("data_test")
    
    print("\n1. Testing Signup...")
    success, msg = auth.signup("testuser", "password123")
    print(f"Signup Result: {success} ({msg})")
    
    print("\n2. Testing Login (Correct Password)...")
    success, msg = auth.login("testuser", "password123")
    print(f"Login Result: {success} ({msg})")
    
    print("\n3. Testing Login (Wrong Password)...")
    success, msg = auth.login("testuser", "wrongpass")
    print(f"Login Result: {success} ({msg})")
    
    print("\n4. Face ID Status...")
    import numpy as np
    try:
        import face_recognition
        print("✅ Face Recognition Library is installed.")
        # Create dummy encoding
        dummy_encoding = np.zeros(128)
        auth.signup("faceuser", "pass", dummy_encoding)
        success, name = auth.login_with_face(dummy_encoding)
        print(f"Face Login Result: {success} ({name})")
    except ImportError:
        print("⚠️ Face Recognition not installed (Expected if on Windows without C++ tools). Fallback active.")

if __name__ == "__main__":
    test_auth()
