"""
Hinglish Processor - Processes Hindi-English mixed language complaints.
"""
import pandas as pd
import re
from typing import List, Dict, Tuple
import os


class HinglishProcessor:
    """Process Hinglish (Hindi-English) text for sentiment analysis."""
    
    def __init__(self):
        """Initialize processor with Hinglish patterns."""
        # Common Hinglish complaint patterns
        self.hinglish_patterns = {
            'negative': [
                r'bekaar|bekaar',  # useless/bad
                r'chor|chor hai',  # thief/cheat
                r'fas gaya|phass gaya',  # got stuck/trapped
                r'dhoka|dhoka diya',  # cheated
                r'loot rahe|loot raha',  # looting/robbing
                r'paise waste|paisa waste',  # money wasted
                r'galat|galat hai',  # wrong
                r'kharab|kharab hai',  # bad
                r'bewakoof|bewakoof banaya',  # fooled
                r'fraud|fraud hai'  # fraud
            ],
            'positive': [
                r'achha|achha hai',  # good
                r'sahi|sahi hai',  # correct
                r'badhiya|badhiya hai',  # great
                r'khush|khush hai',  # happy
                r'satisfied|satisfied hai'  # satisfied
            ],
            'complaint_types': {
                'hidden_charges': [r'hidden charge|hidden fee|chhupa hua charge|extra charge'],
                'poor_returns': [r'return nahi mila|returns nahi|kam return|poor return'],
                'service_issues': [r'bad service|kharab service|response nahi|ignore kar rahe'],
                'misleading': [r'galat promise|false promise|jhoot|lie kiya']
            }
        }
    
    def detect_hinglish(self, text: str) -> bool:
        """Detect if text contains Hinglish."""
        # Check for Devanagari script
        devanagari_pattern = r'[\u0900-\u097F]'
        if re.search(devanagari_pattern, text):
            return True
        
        # Check for common Hinglish words
        hinglish_words = ['hai', 'nahi', 'ki', 'ka', 'se', 'mein', 'ko', 'ke', 'ne']
        text_lower = text.lower()
        return any(word in text_lower for word in hinglish_words) and any(
            char.isalpha() for char in text if ord(char) < 128
        )
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of Hinglish text.
        
        Args:
            text: Input text (may contain Hinglish)
            
        Returns:
            Dictionary with sentiment analysis results
        """
        text_lower = text.lower()
        
        # Count negative patterns
        negative_count = sum(
            len(re.findall(pattern, text_lower, re.IGNORECASE))
            for pattern in self.hinglish_patterns['negative']
        )
        
        # Count positive patterns
        positive_count = sum(
            len(re.findall(pattern, text_lower, re.IGNORECASE))
            for pattern in self.hinglish_patterns['positive']
        )
        
        # Determine sentiment
        if negative_count > positive_count:
            sentiment = 'NEGATIVE'
            sentiment_score = max(0.0, 0.5 - (negative_count * 0.1))
        elif positive_count > negative_count:
            sentiment = 'POSITIVE'
            sentiment_score = min(1.0, 0.5 + (positive_count * 0.1))
        else:
            sentiment = 'NEUTRAL'
            sentiment_score = 0.5
        
        # Detect complaint types
        complaint_types = []
        for complaint_type, patterns in self.hinglish_patterns['complaint_types'].items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    complaint_types.append(complaint_type.replace('_', ' ').title())
                    break
        
        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'negative_indicators': negative_count,
            'positive_indicators': positive_count,
            'complaint_types': complaint_types,
            'is_hinglish': self.detect_hinglish(text)
        }
    
    def translate_key_phrases(self, text: str) -> str:
        """Translate key Hinglish phrases to English for better understanding."""
        translations = {
            'bekaar': 'useless/bad',
            'chor': 'thief/cheat',
            'fas gaya': 'got stuck',
            'dhoka': 'cheated',
            'loot rahe': 'looting',
            'achha': 'good',
            'sahi': 'correct',
            'kharab': 'bad',
            'return nahi mila': 'did not get returns',
            'hidden charge': 'hidden charge',
            'bad service': 'bad service'
        }
        
        text_lower = text.lower()
        translated = text
        for hinglish, english in translations.items():
            if hinglish in text_lower:
                translated += f" [{english}]"
        
        return translated


def process_hinglish_complaints(csv_path: str = "data/mock/customer_reviews.csv",
                                output_path: str = "data/processed/hinglish_analysis.csv"):
    """Process Hinglish complaints from reviews CSV."""
    print("=" * 60)
    print("HINGLISH COMPLAINT ANALYSIS")
    print("=" * 60)
    print()
    
    if not os.path.exists(csv_path):
        print(f"❌ Reviews file not found: {csv_path}")
        print("💡 Run: python mock_data_generator.py")
        return
    
    try:
        reviews_df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    processor = HinglishProcessor()
    
    # Analyze each review
    results = []
    hinglish_count = 0
    
    for idx, row in reviews_df.iterrows():
        text = str(row.get('text', ''))
        if not text or pd.isna(text):
            continue
        
        analysis = processor.analyze_sentiment(text)
        
        if analysis['is_hinglish']:
            hinglish_count += 1
        
        result = {
            'review_id': row.get('review_id', idx),
            'product': row.get('product', 'Unknown'),
            'original_text': text,
            'is_hinglish': analysis['is_hinglish'],
            'sentiment': analysis['sentiment'],
            'sentiment_score': analysis['sentiment_score'],
            'complaint_types': ', '.join(analysis['complaint_types']) if analysis['complaint_types'] else 'None',
            'translated_key_phrases': processor.translate_key_phrases(text)
        }
        results.append(result)
    
    # Save results
    results_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results_df.to_csv(output_path, index=False)
    
    print(f"✅ Analysis complete!")
    print(f"   Total reviews analyzed: {len(results)}")
    print(f"   Hinglish reviews detected: {hinglish_count}")
    print(f"   Negative sentiment: {len([r for r in results if r['sentiment'] == 'NEGATIVE'])}")
    print(f"   Results saved to: {output_path}")
    
    # Show sample analysis
    print("\n" + "=" * 60)
    print("SAMPLE ANALYSIS")
    print("=" * 60)
    
    hinglish_reviews = [r for r in results if r['is_hinglish']][:3]
    for review in hinglish_reviews:
        print(f"\nOriginal: {review['original_text']}")
        print(f"Translated: {review['translated_key_phrases']}")
        print(f"Sentiment: {review['sentiment']} ({review['sentiment_score']:.2f})")
        if review['complaint_types'] != 'None':
            print(f"Complaint Types: {review['complaint_types']}")


if __name__ == "__main__":
    # Sample complaints for testing
    sample_complaints = [
        "Ye policy sabse bekaar hai, paisa phas gaya",
        "Agent ne dhoka diya, returns nahi mila",
        "Bank wale chor hai, hidden charges loot rahe hai",
        "Good product, satisfied customer",
        "Service kharab hai, response nahi mila"
    ]
    
    processor = HinglishProcessor()
    
    print("=" * 60)
    print("HINGLISH COMPLAINT ANALYSIS - DEMO")
    print("=" * 60)
    print()
    
    for complaint in sample_complaints:
        print(f"Original: {complaint}")
        analysis = processor.analyze_sentiment(complaint)
        print(f"Sentiment: {analysis['sentiment']} (Score: {analysis['sentiment_score']:.2f})")
        print(f"Is Hinglish: {analysis['is_hinglish']}")
        if analysis['complaint_types']:
            print(f"Complaint Types: {', '.join(analysis['complaint_types'])}")
        print()
    
    # Process actual CSV if available
    if os.path.exists("data/mock/customer_reviews.csv"):
        print("\n" + "=" * 60)
        print("PROCESSING CSV FILE")
        print("=" * 60)
        process_hinglish_complaints()
    else:
        print("\n💡 To process CSV file:")
        print("   1. Run: python mock_data_generator.py")
        print("   2. Run: python features/hinglish_processor.py")
