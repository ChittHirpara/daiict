# backend/gap_analyzer/gap_detector.py - COMPLETE VERSION
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
import json
import re
import warnings
warnings.filterwarnings('ignore')

@dataclass
class Mismatch:
    promise_aspect: str
    complaint_topic: str
    severity: float  # 0-1
    evidence: List[str]
    mismatch_type: str  # 'direct_contradiction', 'expectation_gap', 'omission'
    confidence: float

@dataclass
class GapAnalysisResult:
    product_name: str
    promise_confidence: float
    sentiment_score: float
    dissatisfaction_index: float
    mismatches: List[Mismatch]
    overall_risk_score: float
    risk_level: str  # 'low', 'medium', 'high', 'critical'
    recommendations: List[str]

class GapDetector:
    def __init__(self):
        # Define mismatch patterns
        self.contradiction_patterns = {
            'returns': {
                'promise_terms': ['return', 'yield', 'profit', 'gain', 'earn', 'income', 'growth'],
                'complaint_terms': ['no return', 'low return', 'loss', 'negative return', 'waste', 'poor returns', 'zero return'],
                'weight': 1.2
            },
            'risk': {
                'promise_terms': ['low risk', 'safe', 'secure', 'protected', 'guaranteed', 'capital protection', 'stable'],
                'complaint_terms': ['risky', 'lost money', 'dangerous', 'unsafe', 'fraud', 'scam', 'cheat', 'volatile'],
                'weight': 1.3
            },
            'fees': {
                'promise_terms': ['no charge', 'low fee', 'free', 'no hidden', 'transparent', 'zero charges', 'no commission'],
                'complaint_terms': ['hidden charge', 'extra fee', 'unexpected cost', 'cheated', 'high fees', 'commission', 'charges'],
                'weight': 1.0
            },
            'service': {
                'promise_terms': ['good service', 'quick service', 'support', 'helpful', 'responsive', '24/7 support', 'dedicated'],
                'complaint_terms': ['bad service', 'no response', 'ignore', 'rude', 'delay', 'poor support', 'unresponsive'],
                'weight': 0.8
            },
            'liquidity': {
                'promise_terms': ['easy exit', 'liquid', 'withdraw anytime', 'flexible', 'no lock-in', 'instant withdrawal'],
                'complaint_terms': ['cannot exit', 'locked', 'withdrawal problem', 'stuck', 'no withdrawal', 'exit blocked'],
                'weight': 0.9
            }
        }
    
    def detect_mismatches(self, promise: Dict, sentiment_result: Dict) -> List[Mismatch]:
        """Detect mismatches between promises and reality"""
        mismatches = []
        
        # Convert promise to searchable text
        promise_text = " ".join([
            str(promise.get('investment_objective', '')),
            str(promise.get('promised_returns', '')),
            str(promise.get('risk_category', '')),
            " ".join(promise.get('key_features', [])),
            " ".join(promise.get('warnings', []))
        ]).lower()
        
        # Get complaint topics from sentiment result
        complaint_topics = sentiment_result.get('top_complaints', [])
        complaint_text = ""
        if isinstance(complaint_topics, list) and len(complaint_topics) > 0:
            # complaint_topics is list of tuples (topic, count)
            complaint_text = " ".join([topic for topic, _ in complaint_topics]).lower()
        
        # Check each contradiction pattern
        for aspect, patterns in self.contradiction_patterns.items():
            # Check if promise makes claims in this aspect
            promise_mentions = any(term in promise_text for term in patterns['promise_terms'])
            
            # Check if complaints contradict
            complaint_mentions = any(term in complaint_text for term in patterns['complaint_terms'])
            
            if promise_mentions and complaint_mentions:
                # Calculate severity based on frequency and sentiment
                severity = self.calculate_severity(aspect, promise_text, complaint_text, sentiment_result)
                
                # Collect evidence
                evidence = self.collect_evidence(aspect, promise, complaint_topics)
                
                mismatch = Mismatch(
                    promise_aspect=aspect.upper(),
                    complaint_topic=self.get_main_complaint(aspect, complaint_topics),
                    severity=severity,
                    evidence=evidence,
                    mismatch_type='direct_contradiction',
                    confidence=min(promise.get('extraction_confidence', 0.5), 0.8)
                )
                mismatches.append(mismatch)
        
        # Additional gap: Promise too good to be true
        if self.is_too_good_to_be_true(promise):
            mismatch = Mismatch(
                promise_aspect='OVERALL',
                complaint_topic='Unrealistic expectations',
                severity=0.7,
                evidence=['Product makes exceptional promises with minimal warnings'],
                mismatch_type='expectation_gap',
                confidence=0.9
            )
            mismatches.append(mismatch)
        
        return mismatches
    
    def calculate_severity(self, aspect: str, promise_text: str, complaint_text: str, sentiment: Dict) -> float:
        """Calculate severity of mismatch (0-1)"""
        base_severity = 0.5
        
        # Adjust based on sentiment
        dissatisfaction = sentiment.get('dissatisfaction_index', 0) / 100
        base_severity += dissatisfaction * 0.3
        
        # Adjust based on aspect importance
        aspect_weight = self.contradiction_patterns[aspect]['weight']
        base_severity *= aspect_weight
        
        # Cap at 1.0
        return min(1.0, base_severity)
    
    def collect_evidence(self, aspect: str, promise: Dict, complaints: List) -> List[str]:
        """Collect specific evidence of mismatch"""
        evidence = []
        
        if aspect == 'returns':
            if promise.get('promised_returns'):
                evidence.append(f"Promised returns: {promise['promised_returns']}")
                evidence.append("Complaints indicate returns not being delivered")
        
        elif aspect == 'risk':
            if promise.get('risk_category'):
                evidence.append(f"Promised risk level: {promise['risk_category']}")
                evidence.append("Customers report unexpected losses or high risk")
        
        elif aspect == 'fees':
            if 'no hidden' in " ".join(promise.get('key_features', [])).lower():
                evidence.append("Promised: No hidden charges")
                evidence.append("Complaints: Customers report hidden fees")
        
        elif aspect == 'service':
            evidence.append("Promised: Good customer service")
            evidence.append("Complaints: Poor service quality reported")
        
        elif aspect == 'liquidity':
            if promise.get('lock_in_period'):
                evidence.append(f"Lock-in period: {promise['lock_in_period']}")
                evidence.append("Complaints: Customers facing exit problems")
        
        return evidence
    
    def get_main_complaint(self, aspect: str, complaints: List) -> str:
        """Extract main complaint related to aspect"""
        if not complaints:
            return "General dissatisfaction"
        
        # Look for aspect-related complaints
        for complaint, count in complaints:
            if aspect in complaint.lower():
                return complaint
        
        # Return first complaint
        return complaints[0][0] if complaints else "Various complaints"
    
    def is_too_good_to_be_true(self, promise: Dict) -> bool:
        """Check if promises seem unrealistic"""
        text = " ".join([
            str(promise.get('investment_objective', '')),
            str(promise.get('promised_returns', '')),
            " ".join(promise.get('key_features', []))
        ]).lower()
        
        # Check for overly optimistic language
        optimistic_terms = ['guaranteed', 'risk-free', '100% safe', 'no risk', 'cannot lose']
        optimistic_count = sum(1 for term in optimistic_terms if term in text)
        
        # Check warnings (fewer warnings = more suspicious)
        warnings = len(promise.get('warnings', []))
        
        return optimistic_count > 1 and warnings < 2
    
    def analyze_gap(self, promise_data: Dict, sentiment_data: Dict) -> GapAnalysisResult:
        """Complete gap analysis for a product"""
        # Detect mismatches
        mismatches = self.detect_mismatches(promise_data, sentiment_data)
        
        # Calculate overall risk score
        risk_score = self.calculate_risk_score(mismatches, sentiment_data)
        
        # Determine risk level
        risk_level = self.determine_risk_level(risk_score)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(mismatches, risk_level)
        
        return GapAnalysisResult(
            product_name=promise_data.get('product_name', 'Unknown'),
            promise_confidence=promise_data.get('extraction_confidence', 0.0),
            sentiment_score=sentiment_data.get('avg_sentiment', 0.5),
            dissatisfaction_index=sentiment_data.get('dissatisfaction_index', 0),
            mismatches=mismatches,
            overall_risk_score=risk_score,
            risk_level=risk_level,
            recommendations=recommendations
        )
    
    def calculate_risk_score(self, mismatches: List[Mismatch], sentiment: Dict) -> float:
        """Calculate overall risk score (0-1)"""
        if not mismatches:
            base_score = 0.2
        else:
            # Average of mismatch severities
            base_score = np.mean([m.severity for m in mismatches])
        
        # Adjust with sentiment
        dissatisfaction = sentiment.get('dissatisfaction_index', 0) / 100
        adjusted_score = base_score * 0.7 + dissatisfaction * 0.3
        
        return min(1.0, adjusted_score)
    
    def determine_risk_level(self, risk_score: float) -> str:
        """Convert risk score to risk level"""
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.6:
            return 'medium'
        elif risk_score < 0.8:
            return 'high'
        else:
            return 'critical'
    
    def generate_recommendations(self, mismatches: List[Mismatch], risk_level: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # General recommendations based on risk level
        if risk_level == 'critical':
            recommendations.append("🚨 IMMEDIATE REGULATOR INVESTIGATION REQUIRED")
            recommendations.append("Issue public warning about this product")
            recommendations.append("Freeze new sales until investigation complete")
        elif risk_level == 'high':
            recommendations.append("⚠️ High priority review needed")
            recommendations.append("Request detailed explanation from product issuer")
            recommendations.append("Monitor social media for emerging complaints")
        elif risk_level == 'medium':
            recommendations.append("📊 Regular monitoring recommended")
            recommendations.append("Require clearer disclosure documents")
            recommendations.append("Sample audit of customer experiences")
        
        # Specific recommendations based on mismatches
        for mismatch in mismatches:
            if mismatch.promise_aspect == 'RETURNS':
                recommendations.append(f"Verify actual returns vs promised {mismatch.promise_aspect}")
            elif mismatch.promise_aspect == 'RISK':
                recommendations.append(f"Review risk disclosure adequacy")
            elif mismatch.promise_aspect == 'FEES':
                recommendations.append(f"Audit fee structure and disclosures")
        
        # Always recommend transparency
        recommendations.append("Improve transparency in marketing materials")
        recommendations.append("Enhance customer complaint resolution process")
        
        return recommendations[:5]  # Return top 5 recommendations

# Test the gap detector
if __name__ == "__main__":
    print("=" * 60)
    print("GAP DETECTOR TEST")
    print("=" * 60)
    
    detector = GapDetector()
    
    # Sample promise data
    sample_promise = {
        'product_name': 'Alpha Growth Mutual Fund',
        'issuer': 'HDFC',
        'investment_objective': 'To generate high returns',
        'promised_returns': '15%',
        'risk_category': 'Low',
        'lock_in_period': '3 years',
        'exit_load': '1%',
        'min_investment': '₹5000',
        'key_features': ['High returns', 'Low risk', 'No hidden charges'],
        'warnings': ['Market risks apply'],
        'extraction_confidence': 0.85
    }
    
    # Sample sentiment data
    sample_sentiment = {
        'product': 'Alpha Growth Mutual Fund',
        'avg_sentiment': 0.3,
        'dissatisfaction_index': 75.0,
        'top_complaints': [('hidden charges complaints', 15), ('poor returns issue', 12), ('bad service', 8)]
    }
    
    print("\nAnalyzing gap between promise and reality...")
    result = detector.analyze_gap(sample_promise, sample_sentiment)
    
    print(f"\n📋 Product: {result.product_name}")
    print(f"📊 Risk Level: {result.risk_level.upper()} (Score: {result.overall_risk_score:.2f})")
    print(f"😊 Sentiment Score: {result.sentiment_score:.2f}")
    print(f"😠 Dissatisfaction Index: {result.dissatisfaction_index:.1f}%")
    
    print(f"\n🔍 Mismatches Found: {len(result.mismatches)}")
    for i, mismatch in enumerate(result.mismatches, 1):
        print(f"\n  {i}. {mismatch.promise_aspect} MISMATCH")
        print(f"     Complaint: {mismatch.complaint_topic}")
        print(f"     Severity: {mismatch.severity:.2f}")
        print(f"     Type: {mismatch.mismatch_type}")
        print(f"     Evidence: {', '.join(mismatch.evidence[:2])}")
    
    print(f"\n💡 Recommendations:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")
    
    print("\n✅ Gap analysis complete!")