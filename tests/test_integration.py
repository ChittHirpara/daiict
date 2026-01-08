"""
Integration tests for end-to-end functionality
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.db_manager import DatabaseManager
from backend.expectation_engine.promise_extractor import PromiseExtractor
from backend.reality_engine.sentiment_analyzer import AdvancedSentimentAnalyzer
from backend.gap_analyzer.gap_detector import GapDetector


class TestIntegration(unittest.TestCase):
    """End-to-end integration tests"""
    
    def setUp(self):
        """Setup test environment"""
        # Initialize database tables
        from database.schema import Base, create_engine_instance
        engine = create_engine_instance()
        Base.metadata.create_all(engine)
        self.db = DatabaseManager()
        self.extractor = PromiseExtractor()
        # Skip sentiment analyzer if dependencies not available
        try:
            self.sentiment_analyzer = AdvancedSentimentAnalyzer()
        except Exception:
            self.sentiment_analyzer = None
        self.gap_detector = GapDetector()
    
    def tearDown(self):
        """Cleanup"""
        self.db.close()
    
    def test_full_pipeline(self):
        """Test complete pipeline from extraction to gap analysis"""
        # 1. Create product
        product = self.db.get_or_create_product(
            name="Test Integration Product",
            category="Mutual Fund",
            issuer="Test Bank"
        )
        self.assertIsNotNone(product)
        
        # 2. Extract promise
        test_text = "Product promises 12% returns with low risk, 3 year lock-in"
        promise = self.extractor.extract_from_text(
            test_text,
            {'product_name': product.name, 'issuer': 'Test Bank'}
        )
        
        # Save promise
        promise_data = {
            'investment_objective': promise.investment_objective,
            'promised_returns': promise.promised_returns,
            'risk_category': promise.risk_category,
            'lock_in_period': promise.lock_in_period,
            'extraction_confidence': promise.extraction_confidence
        }
        db_promise = self.db.save_promise(product.id, promise_data)
        self.assertIsNotNone(db_promise)
        
        # 3. Analyze sentiment
        if self.sentiment_analyzer is None:
            self.skipTest("Sentiment analyzer not available")
        
        test_reviews = [
            "Great product, very satisfied!",
            "Not getting promised returns, disappointed",
            "Hidden charges everywhere"
        ]
        
        sentiment_results = []
        for review in test_reviews:
            sentiment = self.sentiment_analyzer.analyze_sentiment(review)
            sentiment_results.append(sentiment)
        
        # Save sentiment analysis
        # analyze_sentiment returns 'sentiment_value' (0.0 for negative, 1.0 for positive)
        # Convert to -1 to 1 scale
        sentiment_values = [s['sentiment_value'] * 2 - 1 for s in sentiment_results]
        avg_sentiment = sum(sentiment_values) / len(sentiment_values)
        sentiment_data = {
            'avg_sentiment': avg_sentiment,
            'positive_count': sum(1 for s in sentiment_values if s > 0.2),
            'negative_count': sum(1 for s in sentiment_values if s < -0.2),
            'neutral_count': sum(1 for s in sentiment_values if -0.2 <= s <= 0.2),
            'total_reviews': len(test_reviews),
            'dissatisfaction_index': 40.0
        }
        sentiment_analysis = self.db.save_sentiment_analysis(product.id, sentiment_data)
        self.assertIsNotNone(sentiment_analysis)
        
        # 4. Detect gap
        promise_dict = {
            'promised_returns': promise.promised_returns or '12%',
            'risk_category': promise.risk_category
        }
        sentiment_dict = {
            'avg_sentiment': avg_sentiment,
            'dissatisfaction_index': sentiment_analysis.dissatisfaction_index,
            'complaints': ['No returns', 'Hidden charges']
        }
        
        gap_result = self.gap_detector.analyze_gap(promise_dict, sentiment_dict)
        self.assertIsNotNone(gap_result)
        
        # Save gap analysis
        gap_data = {
            'promise_confidence': promise.extraction_confidence,
            'sentiment_score': avg_sentiment,
            'dissatisfaction_index': sentiment_analysis.dissatisfaction_index,
            'overall_risk_score': gap_result.overall_risk_score,
            'risk_level': gap_result.risk_level,
            'mismatches': [m.__dict__ for m in gap_result.mismatches],
            'recommendations': gap_result.recommendations
        }
        gap_analysis = self.db.save_gap_analysis(product.id, gap_data)
        self.assertIsNotNone(gap_analysis)
        
        # Verify complete pipeline
        self.assertGreater(gap_result.overall_risk_score, 0)
        self.assertIn(gap_result.risk_level, ['low', 'medium', 'high', 'critical'])


if __name__ == '__main__':
    unittest.main()
