import os
import json
import bcrypt
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Tuple

# Replace face_recognition with cv2
try:
    import cv2
    FACE_AUTH_AVAILABLE = True
except ImportError:
    FACE_AUTH_AVAILABLE = False
    print("⚠️ OpenCV library not available. Face ID features disabled.")

class AuthManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.users_file = self.data_dir / "users.json"
        self._ensure_data_dir()
        self.users = self._load_users()

    def _ensure_data_dir(self):
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self) -> Dict:
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)

    def signup(self, username, password, face_encoding=None) -> Tuple[bool, str]:
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"

        # Hash password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'password_hash': hashed.decode('utf-8'),
            'has_face_id': False
        }

        # Store face encoding if provided
        if face_encoding is not None and FACE_AUTH_AVAILABLE:
            # Convert numpy array to list for JSON serialization
            if isinstance(face_encoding, np.ndarray):
                user_data['face_encoding'] = face_encoding.tolist()
            else:
                user_data['face_encoding'] = face_encoding
            user_data['has_face_id'] = True

        self.users[username] = user_data
        self._save_users()
        return True, "User created successfully"

    def login(self, username, password) -> Tuple[bool, str]:
        """Login with password"""
        if username not in self.users:
            return False, "User not found"

        stored_hash = self.users[username]['password_hash'].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return True, "Login successful"
        
        return False, "Incorrect password"

    def login_with_face(self, input_face_encoding) -> Tuple[bool, str]:
        """Login by comparing face encoding with all users"""
        if not FACE_AUTH_AVAILABLE:
            return False, "Face ID system not available"

        if input_face_encoding is None:
            return False, "No face detected"

        input_hist = np.array(input_face_encoding, dtype=np.float32)

        # Check against all users with face ID
        best_score = -1
        best_user = None

        for username, data in self.users.items():
            if data.get('has_face_id') and 'face_encoding' in data:
                stored_hist = np.array(data['face_encoding'], dtype=np.float32)
                
                # Compare Histograms (Correlation: 1.0 is perfect match)
                score = cv2.compareHist(input_hist, stored_hist, cv2.HISTCMP_CORREL)
                
                if score > best_score:
                    best_score = score
                    best_user = username

        # Threshold for match (0.5 is a reasonable heuristic for histograms of same face in flux)
        # Note: This is simpler than dlib but works for basic demos
        if best_score > 0.5:
             return True, best_user

        return False, "Face not recognized"

    def get_face_encoding_from_image(self, image_array):
        """Process image to get encoding using OpenCV (Histogram)"""
        if not FACE_AUTH_AVAILABLE:
            return None
            
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            
            # Load Haar Cascade
            # Try getting path from cv2.data
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            face_cascade = cv2.CascadeClassifier(cascade_path)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return None
                
            # Take the largest face
            faces = sorted(faces, key=lambda x: x[2]*x[3], reverse=True)
            x, y, w, h = faces[0]
            
            # Extract ROI
            roi = gray[y:y+h, x:x+w]
            
            # Calculate Histogram as 128 encoding
            hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
            
            return hist.flatten()
            
        except Exception as e:
            print(f"Error processing face: {e}")
            
        return None

    def get_users(self) -> Dict:
        """Get all registered users (safe view)"""
        safe_users = {}
        for user, data in self.users.items():
            safe_users[user] = {
                "has_face_id": data.get('has_face_id', False),
                "joined": "Unknown" # Placeholder, could add timestamp later
            }
        return safe_users

    def delete_user(self, username: str) -> bool:
        """Delete a user"""
        if username in self.users:
            del self.users[username]
            self._save_users()
            return True
        return False

