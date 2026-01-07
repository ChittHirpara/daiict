# backend/expectation_engine/promise_extractor.py - UPDATED VERSION
try:
    import spacy
except (ImportError, Exception) as e:
    print(f"[WARNING] Failed to import spacy ({e}). using regex fallback.")
    spacy = None

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import pandas as pd
import os
from pathlib import Path
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

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
        self.nlp = None
        if spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except:
                print("[WARNING] Could not load spaCy model. Using regex fallback.")
                try:
                    # Try downloading if not present
                    print("Attempting to download spaCy model...")
                    os.system("python -m spacy download en_core_web_sm")
                    self.nlp = spacy.load("en_core_web_sm")
                except:
                    print("[ERROR] Failed to load spaCy. Will use basic text processing.")
        else:
            print("[WARNING] Spacy not available. Using regex fallback.")
        
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
        
        # Sentence splitting (Spacy or Simple)
        sentences = []
        if self.nlp:
            try:
                doc = self.nlp(text)
                sentences = [sent.text.strip() for sent in doc.sents]
                
                # Extract key features and warnings using NLP
                for sent in doc.sents:
                    sent_text = sent.text.lower()
                    # Key features (positive assertions)
                    if any(word in sent_text for word in ['feature', 'benefit', 'advantage', 'include', 'offer']):
                        if len(sent_text.split()) < 20:
                            extraction['key_features'].append(sent.text)
                    
                    # Warnings
                    if any(word in sent_text for word in ['warning', 'risk', 'caution', 'note:', 'important:', 'disclaimer']):
                        extraction['warnings'].append(sent.text)
            except:
                sentences = [s.strip() for s in text.split('.') if s.strip()]
        else:
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            # Simple fallback for features/warnings
            for sent in sentences:
                sent_lower = sent.lower()
                if any(word in sent_lower for word in ['feature', 'benefit', 'advantage']):
                    extraction['key_features'].append(sent)
                if any(word in sent_lower for word in ['warning', 'risk', 'caution']):
                    extraction['warnings'].append(sent)
        
        # Find investment objective (usually first sentence)
        if sentences:
            extraction['investment_objective'] = sentences[0]
        
        # Extract using patterns (Robust Regex)
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
        
        # Calculate confidence
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
    
    def extract_from_pdf(self, pdf_path: str) -> FinancialPromise:
        """Extract promises from PDF file"""
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is not installed. Please install it using 'pip install PyPDF2'")
            
        print(f"Reading PDF: {pdf_path}")
        text = ""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return None

        # Basic cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Infer product info from filename
        filename = os.path.basename(pdf_path)
        product_name = os.path.splitext(filename)[0].replace('_', ' ').title()
        
        product_info = {
            'product_name': product_name,
            'issuer': 'Detected from PDF' 
        }
        
        return self.extract_from_text(text, product_info)
    
    def batch_extract(self, data_dir: str) -> pd.DataFrame:
        """Extract promises from multiple documents (JSON and PDF)"""
        import glob
        
        promises = []
        
        # Process JSON files (Simulated docs)
        for file_path in glob.glob(os.path.join(data_dir, "*.json")):
            try:
                promise = self.extract_from_json(file_path)
                promises.append(asdict(promise))
                print(f"✓ Extracted (JSON): {os.path.basename(file_path)}")
            except Exception as e:
                print(f"✗ Error processing {file_path}: {e}")

        # Process PDF files (Real docs)
        for file_path in glob.glob(os.path.join(data_dir, "*.pdf")):
            try:
                promise = self.extract_from_pdf(file_path)
                if promise:
                    promises.append(asdict(promise))
                    print(f"✓ Extracted (PDF): {os.path.basename(file_path)}")
            except Exception as e:
                print(f"✗ Error processing {file_path}: {e}")
        
        if not promises:
            return pd.DataFrame() # Return empty if no promises found

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
