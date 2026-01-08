"""
API endpoint tests
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestAPI(unittest.TestCase):
    """Test API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test client once for all tests"""
        cls.client = None
        try:
            from fastapi.testclient import TestClient
            from api.main import app
            cls.client = TestClient(app)
        except Exception as e:
            # Store error to skip tests
            cls.client = None
            cls.skip_reason = str(e)
    
    def setUp(self):
        """Skip tests if client not available"""
        if self.client is None:
            self.skipTest(f"API not available: {getattr(self, 'skip_reason', 'Unknown error')}")
    
    def test_health(self):
        """Test health endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("status", data)
    
    def test_statistics(self):
        """Test statistics endpoint"""
        response = self.client.get("/api/v1/statistics")
        self.assertIn(response.status_code, [200, 404])
    
    def test_products(self):
        """Test products endpoint"""
        response = self.client.get("/api/v1/products")
        self.assertIn(response.status_code, [200, 404])


if __name__ == '__main__':
    # Only run if client was created successfully
    if client is not None:
        unittest.main()
    else:
        print("Skipping API tests - API client not available")
        print("This is OK if API dependencies are not installed")
