import sys
import os
import numpy as np

def verify_face_id():
    print("👤 Verifying Face ID Capability...")
    
    # 1. Check OpenCV
    try:
        import cv2
        print(f"✅ OpenCV installed: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV NOT installed. Face ID will fail.")
        return False

    # 2. Check AuthManager Import
    try:
        sys.path.append(os.getcwd())
        from backend.auth.auth_manager import AuthManager
        print("✅ AuthManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import AuthManager: {e}")
        return False

    # 3. Initialize AuthManager
    try:
        auth = AuthManager()
        print("✅ AuthManager initialized")
    except Exception as e:
        print(f"❌ Failed to initialize AuthManager: {e}")
        return False

    # 4. Check Face Auth Availability Flag
    from backend.auth.auth_manager import FACE_AUTH_AVAILABLE
    if FACE_AUTH_AVAILABLE:
        print("✅ FACE_AUTH_AVAILABLE is True")
    else:
        print("❌ FACE_AUTH_AVAILABLE is False")
        return False

    # 5. Test Encoding Generation (with dummy image)
    print("\n🧪 Testing Encoding Generation...")
    # Create a blank black image (should not find valid face, but shouldn't crash)
    dummy_image = np.zeros((300, 300, 3), dtype=np.uint8)
    
    try:
        encoding = auth.get_face_encoding_from_image(dummy_image)
        if encoding is None:
            print("✅ handled no-face image correctly (returned None)")
        else:
            print(f"⚠️ Warning: Found face in black image? (returned {type(encoding)})")
            
    except Exception as e:
        print(f"❌ Error during encoding generation: {e}")
        return False

    print("\n✨ Face ID Pipeline Verification passed basic checks.")
    print("   (Note: Actual face detection requires a real camera image)")
    return True

if __name__ == "__main__":
    verify_face_id()
