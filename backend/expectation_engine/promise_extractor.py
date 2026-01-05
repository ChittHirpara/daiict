# backend/expectation_engine/promise_extractor.py - CORRECTED VERSION
import spacy
import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import os
from pathlib import Path

@dataclass
class FinancialPromise:
    product_name: str
    issuer: str
    investment_objective: str
    promised_returns: Optional[str]
    risk_category: str
    lock_in_period: Optional[str]
    exit_load: Optional[str]
    min_investment: Optional[str]
    key_features: List[str]
    warnings: List[str]
    extraction_confidence: float

class PromiseExtractor:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spaCy model...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Define regex patterns for financial terms
        self.patterns = {
            'returns': [
                r'(\d+(\.\d+)?)%\s*(p\.a\.|per annum|annual|yearly)',
                r'returns?\s*(?:of|up to|around)\s*(\d+(\.\d+)?)%',
                r'earn\s*(?:up to\s*)?(\d+(\.\d+)?)%',
                r'yield\s*(?:of\s*)?(\d+(\.\d+)?)%'
            ],
            'risk': [
                r'(low|moderate|high|very high)\s*risk',
                r'risk\s*(?:level|category|profile):?\s*(low|moderate|high)',
                r'capital\s+protection',
                r'principal\s+guaranteed'
            ],
            'lock_in': [
                r'lock[-\s]*in\s*(?:period)?:?\s*(\d+)\s*(?:years?|months?)',
                r'maturity[:\s]*(\d+)\s*(?:years?|months?)',
                r'minimum\s*tenure:?\s*(\d+)\s*(?:years?|months?)'
            ],
            'fees': [
                r'exit\s*load:?\s*(\d+(\.\d+)?)%',
                r'early\s*withdrawal\s*charge:?\s*(\d+(\.\d+)?)%',
                r'management\s*fee:?\s*(\d+(\.\d+)?)%'
            ],
            'investment': [
                r'minimum\s*investment:?\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'invest\s*as\s*low\s*as\s*[₹$]?\s*(\d+(?:,\d+)*(?:\.\d+)?)'
            ]
        }
        
    def extract_from_text(self, text: str, product_info: Dict = None) -> FinancialPromise:
        """Extract promises from text"""
        doc = self.nlp(text)
        
        # Initialize extraction
        extraction = {
            'product_name': product_info.get('product_name', 'Unknown') if product_info else 'Unknown',
            'issuer': product_info.get('issuer', 'Unknown') if product_info else 'Unknown',
            'investment_objective': '',
            'promised_returns': None,
            'risk_category': 'Unknown',
            'lock_in_period': None,
            'exit_load': None,
            'min_investment': None,
            'key_features': [],
            'warnings': [],
            'extraction_confidence': 0.0
        }
        
        # Find investment objective (usually first sentence or specific phrases)
        sentences = [sent.text.strip() for sent in doc.sents]
        if sentences:
            extraction['investment_objective'] = sentences[0]
        
        # Extract using patterns
        for category, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    if category == 'returns':
                        extraction['promised_returns'] = f"{match.group(1)}%"
                    elif category == 'risk':
                        extraction['risk_category'] = match.group(1).title()
                    elif category == 'lock_in':
                        extraction['lock_in_period'] = f"{match.group(1)} years"
                    elif category == 'fees':
                        if 'exit' in match.group(0).lower():
                            extraction['exit_load'] = f"{match.group(1)}%"
                    elif category == 'investment':
                        extraction['min_investment'] = f"₹{match.group(1)}"
        
        # Extract key features and warnings using NLP
        for sent in doc.sents:
            sent_text = sent.text.lower()
            # Key features (positive assertions)
            if any(word in sent_text for word in ['feature', 'benefit', 'advantage', 'include', 'offer']):
                if len(sent_text.split()) < 20:  # Avoid long sentences
                    extraction['key_features'].append(sent.text)
            
            # Warnings (cautions, risks)
            if any(word in sent_text for word in ['warning', 'risk', 'caution', 'note:', 'important:', 'disclaimer']):
                extraction['warnings'].append(sent.text)
        
        # Calculate confidence (simple heuristic)
        confidence_factors = []
        if extraction['investment_objective']: confidence_factors.append(0.2)
        if extraction['promised_returns']: confidence_factors.append(0.2)
        if extraction['risk_category'] != 'Unknown': confidence_factors.append(0.2)
        if extraction['key_features']: confidence_factors.append(0.2)
        if extraction['warnings']: confidence_factors.append(0.2)
        
        extraction['extraction_confidence'] = sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0
        
        return FinancialPromise(**extraction)
    
    def extract_from_json(self, json_path: str) -> FinancialPromise:
        """Extract from JSON document (simulating PDF extraction)"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON to text for extraction
        text_parts = []
        for key, value in data.items():
            if isinstance(value, list):
                text_parts.append(f"{key}: {', '.join(value)}")
            else:
                text_parts.append(f"{key}: {value}")
        
        text = "\n".join(text_parts)
        return self.extract_from_text(text, data)
    
    def batch_extract(self, data_dir: str) -> pd.DataFrame:
        """Extract promises from multiple documents"""
        import glob
        
        promises = []
        for file_path in glob.glob(os.path.join(data_dir, "*.json")):
            try:
                promise = self.extract_from_json(file_path)
                promises.append(asdict(promise))
                print(f"✓ Extracted: {os.path.basename(file_path)}")
            except Exception as e:
                print(f"✗ Error processing {file_path}: {e}")
        
        return pd.DataFrame(promises)

# Test the extractor
if __name__ == "__main__":
    print("=" * 60)
    print("PROMISE EXTRACTOR TEST")
    print("=" * 60)
    
    extractor = PromiseExtractor()
    
    # Test with sample text
    sample_text = """
    Alpha Growth Mutual Fund aims to provide capital appreciation by investing in equity and equity-related instruments.
    The fund targets returns of 12% p.a. over a 5-year period.
    Risk Category: High
    Lock-in period: 3 years
    Exit load: 1% if redeemed before 1 year
    Minimum investment: ₹5000
    Key Features: Tax benefits under section 80C, SIP available
    Warning: Returns are not guaranteed. Past performance is not indicative of future results.
    """
    
    print("\n1. Testing with sample text...")
    promise = extractor.extract_from_text(sample_text)
    print("Extracted Promise:")
    print(json.dumps(asdict(promise), indent=2))
    
    # Test batch extraction
    print("\n2. Testing batch extraction from mock data...")
    data_dir = "data/mock/product_docs"
    
    if os.path.exists(data_dir):
        df = extractor.batch_extract(data_dir)
        print(f"\nExtracted {len(df)} promises")
        
        # Save to CSV
        output_dir = "data/processed"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "extracted_promises.csv")
        df.to_csv(output_path, index=False)
        print(f"Saved to: {output_path}")
        
        # Show preview
        print("\nPreview of extracted promises:")
        print(df.head())
    else:
        print(f"Data directory not found: {data_dir}")
        print("Please run mock_data_generator.py first")
    
    print("\n✅ Promise extraction complete!")