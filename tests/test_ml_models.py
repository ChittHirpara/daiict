"""
ML model tests
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.expectation_engine.promise_extractor import PromiseExtractor
from backend.reality_engine.sentiment_analyzer import AdvancedSentimentAnalyzer
from backend.gap_analyzer.gap_detector import GapDetector


class TestMLModels(unittest.TestCase):
    """Test ML model components"""
    
    def test_promise_extractor(self):
        """Test promise extraction"""
        extractor = PromiseExtractor()
        test_text = """
        Product: Growth Mutual Fund
        Returns: 15% annual
        Risk: High
        Lock-in: 3 years
        """
        result = extractor.extract_from_text(test_text)
        self.assertIsNotNone(result)
        self.assertGreater(result.extraction_confidence, 0)
    
    def test_sentiment_analyzer(self):
        """Test sentiment analysis"""
        analyzer = AdvancedSentimentAnalyzer()
        test_review = "This product is great! Very satisfied with returns."
        sentiment = analyzer.analyze_sentiment(test_review)
        self.assertIsNotNone(sentiment)
        self.assertIn('sentiment_value', sentiment)
    
    def test_gap_detector(self):
        """Test gap detection"""
        detector = GapDetector()
        promise_data = {
            'promised_returns': '15%',
            'risk_category': 'Low'
        }
        sentiment_data = {
            'avg_sentiment': -0.5,
            'dissatisfaction_index': 70,
            'complaints': ['No returns', 'Lost money']
        }
        gap = detector.analyze_gap(promise_data, sentiment_data)
        self.assertIsNotNone(gap)
        self.assertIsNotNone(gap.overall_risk_score)
        self.assertIn(gap.risk_level, ['low', 'medium', 'high', 'critical'])


if __name__ == '__main__':
    unittest.main()
