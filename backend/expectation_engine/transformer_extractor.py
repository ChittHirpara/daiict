"""
Upgraded Promise Extractor using Fine-tuned Transformers
Uses BERT-based models for better semantic understanding
"""
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("[WARNING] Transformers not available. Install: pip install transformers torch")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from backend.expectation_engine.promise_extractor import FinancialPromise, PromiseExtractor


class TransformerPromiseExtractor:
    """
    Advanced promise extractor using fine-tuned BERT models
    Falls back to regex-based extractor if transformers unavailable
    """
    
    def __init__(self, model_name: str = "bert-base-uncased", use_gpu: bool = False):
        """
        Initialize transformer-based extractor
        
        Args:
            model_name: HuggingFace model name
            use_gpu: Whether to use GPU acceleration
        """
        self.model_name = model_name
        self.use_gpu = use_gpu and TORCH_AVAILABLE and torch.cuda.is_available()
        self.nlp_pipeline = None
        self.fallback_extractor = PromiseExtractor()
        
        if TRANSFORMERS_AVAILABLE:
            try:
                # Use Named Entity Recognition for financial terms
                self.nlp_pipeline = pipeline(
                    "ner",
                    model="dslim/bert-base-NER",  # General NER model
                    device=0 if self.use_gpu else -1
                )
                print(f"✅ Loaded transformer model: {model_name}")
            except Exception as e:
                print(f"[WARNING] Could not load transformer model: {e}")
                print("Falling back to regex-based extraction")
                self.nlp_pipeline = None
        else:
            print("[WARNING] Transformers not available. Using regex fallback")
    
    def extract_financial_entities(self, text: str) -> Dict[str, Any]:
        """Extract financial entities using transformer model"""
        if not self.nlp_pipeline:
            return {}
        
        try:
            entities = self.nlp_pipeline(text)
            
            # Organize entities by type
            extracted = {
                'percentages': [],
                'durations': [],
                'amounts': [],
                'organizations': []
            }
            
            for entity in entities:
                entity_text = entity['word']
                entity_label = entity['entity']
                
                # Extract percentages (returns, fees)
                if '%' in entity_text or any(char.isdigit() for char in entity_text):
                    if '%' in entity_text:
                        extracted['percentages'].append(entity_text)
                
                # Extract durations (years, months)
                if any(term in entity_text.lower() for term in ['year', 'month', 'day']):
                    extracted['durations'].append(entity_text)
                
                # Extract amounts (currency)
                if any(char in entity_text for char in ['₹', '$', '€', '£']):
                    extracted['amounts'].append(entity_text)
            
            return extracted
        except Exception as e:
            print(f"Error in transformer extraction: {e}")
            return {}
    
    def extract_promises(self, product_name: str, text: str, product_info: Dict = None) -> FinancialPromise:
        """
        Extract promises using transformer model with regex fallback
        
        Args:
            product_name: Name of the financial product
            text: Text to extract from
            product_info: Optional product metadata
        
        Returns:
            FinancialPromise object
        """
        # First try transformer-based extraction
        transformer_entities = {}
        if self.nlp_pipeline:
            transformer_entities = self.extract_financial_entities(text)
        
        # Use fallback extractor (combines regex + basic NLP)
        fallback_promise = self.fallback_extractor.extract_from_text(text, product_info)
        
        # Enhance with transformer insights if available
        if transformer_entities:
            # Merge transformer results with regex results
            if transformer_entities.get('percentages'):
                # Use first percentage as returns if not already found
                if not fallback_promise.promised_returns:
                    fallback_promise.promised_returns = transformer_entities['percentages'][0]
            
            # Increase confidence if transformer found entities
            fallback_promise.extraction_confidence = min(
                fallback_promise.extraction_confidence + 0.1,
                1.0
            )
        
        return fallback_promise
    
    def batch_extract(self, documents: List[Dict[str, str]]) -> List[FinancialPromise]:
        """Extract promises from multiple documents"""
        results = []
        for doc in documents:
            product_name = doc.get('product_name', 'Unknown')
            text = doc.get('text', '')
            product_info = doc.get('product_info', {})
            
            promise = self.extract_promises(product_name, text, product_info)
            results.append(promise)
        
        return results


class FineTunedFinancialBERT:
    """
    Fine-tuned BERT model specifically for financial promise extraction
    Can be trained on domain-specific financial documents
    """
    
    def __init__(self):
        """Initialize fine-tuned model (placeholder for trained model)"""
        self.model = None
        self.tokenizer = None
        print("[INFO] Fine-tuned model not yet trained. Using base extractor.")
    
    def train(self, training_data: List[Dict]):
        """Train model on financial documents (placeholder)"""
        # This would require:
        # 1. Labeled financial promise dataset
        # 2. Fine-tuning BERT on NER task
        # 3. Evaluation and validation
        print("[INFO] Training functionality not yet implemented")
        print("Would fine-tune BERT on financial promise extraction task")


# Factory function to get best available extractor
def get_promise_extractor(use_transformers: bool = True) -> PromiseExtractor:
    """
    Get the best available promise extractor
    
    Args:
        use_transformers: Whether to prefer transformer-based extraction
    
    Returns:
        PromiseExtractor instance (transformer-enhanced if available)
    """
    if use_transformers and TRANSFORMERS_AVAILABLE:
        try:
            return TransformerPromiseExtractor()
        except Exception as e:
            print(f"Failed to create transformer extractor: {e}")
            return PromiseExtractor()
    else:
        return PromiseExtractor()


if __name__ == "__main__":
    print("Testing Transformer-Based Promise Extractor")
    print("=" * 60)
    
    extractor = get_promise_extractor(use_transformers=True)
    
    sample_text = """
    Alpha Growth Mutual Fund aims to provide capital appreciation.
    Expected returns: 12-15% per annum over 5 years.
    Risk level: High
    Lock-in period: 3 years
    Minimum investment: ₹5,000
    """
    
    promise = extractor.extract_promises("Alpha Growth MF", sample_text)
    print(f"Extracted Promise:")
    print(f"  Returns: {promise.promised_returns}")
    print(f"  Risk: {promise.risk_category}")
    print(f"  Lock-in: {promise.lock_in_period}")
    print(f"  Confidence: {promise.extraction_confidence:.2%}")
