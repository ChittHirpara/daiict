"""
Comprehensive database tests
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import DatabaseManager
from database.schema import Product, Promise, SentimentAnalysis, GapAnalysis


class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Setup test database"""
        # Initialize database tables
        from database.schema import Base, create_engine_instance
        engine = create_engine_instance()
        Base.metadata.create_all(engine)
        self.db = DatabaseManager()
    
    def tearDown(self):
        """Cleanup"""
        self.db.close()
    
    def test_create_product(self):
        """Test creating a product"""
        product = self.db.get_or_create_product(
            name="Test Product",
            category="Mutual Fund",
            issuer="Test Bank"
        )
        self.assertIsNotNone(product)
        self.assertEqual(product.name, "Test Product")
    
    def test_get_product(self):
        """Test retrieving a product"""
        product = self.db.get_or_create_product(
            name="Test Get Product",
            category="Insurance",
            issuer="Test Company"
        )
        retrieved = self.db.get_product_by_id(product.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "Test Get Product")
    
    def test_create_promise(self):
        """Test creating a promise"""
        product = self.db.get_or_create_product(
            name="Promise Test Product",
            category="MF",
            issuer="Test"
        )
        promise_data = {
            'investment_objective': 'Growth',
            'promised_returns': '12%',
            'risk_category': 'High',
            'extraction_confidence': 0.95
        }
        promise = self.db.save_promise(product.id, promise_data)
        self.assertIsNotNone(promise)
        self.assertEqual(promise.promised_returns, "12%")
    
    def test_statistics(self):
        """Test statistics retrieval"""
        stats = self.db.get_statistics()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_products', stats)
        # Check for any of the actual keys returned
        self.assertTrue(len(stats) > 0)
        # Statistics should have numeric values
        if 'total_products' in stats:
            self.assertIsInstance(stats['total_products'], int)


if __name__ == '__main__':
    unittest.main()
