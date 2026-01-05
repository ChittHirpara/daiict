"""
Influencer Tracker - Tracks financial influencers promoting products vs actual customer experience.
"""
import pandas as pd
import json
from typing import Dict, List, Tuple
import os
from datetime import datetime


class InfluencerTracker:
    """Track influencer promotions against customer reality."""
    
    def __init__(self):
        """Initialize tracker with sample influencer data."""
        # Sample influencer database (in production, this would come from API)
        self.influencers = {
            "@FinExpert": {
                "followers": 500000,
                "verified": True,
                "promotions": []
            },
            "@MoneyGuru": {
                "followers": 300000,
                "verified": True,
                "promotions": []
            },
            "@InvestSmart": {
                "followers": 200000,
                "verified": False,
                "promotions": []
            }
        }
    
    def analyze_influencer_promotions(self, gap_df: pd.DataFrame, 
                                      sentiment_df: pd.DataFrame) -> List[Dict]:
        """
        Analyze influencer promotions against customer reality.
        
        Args:
            gap_df: Gap analysis DataFrame
            sentiment_df: Sentiment analysis DataFrame
            
        Returns:
            List of influencer analysis results
        """
        results = []
        
        # Sample influencer-product mappings (in production, extract from social media)
        influencer_products = {
            "@FinExpert": ["Alpha Growth Mutual Fund", "MaxReturns Fixed Deposit"],
            "@MoneyGuru": ["SecureLife Insurance Policy", "WealthBuilder Pension Plan"],
            "@InvestSmart": ["EasyInvest Savings Account"]
        }
        
        for influencer, products in influencer_products.items():
            for product in products:
                # Find product in gap analysis
                product_data = gap_df[gap_df['product_name'] == product]
                
                if len(product_data) > 0:
                    row = product_data.iloc[0]
                    risk_level = str(row.get('risk_level', 'medium')).lower()
                    risk_score = float(row.get('overall_risk_score', 0.5))
                    dissatisfaction = float(row.get('dissatisfaction_index', 0))
                    
                    # Determine if influencer promotion is misleading
                    is_misleading = risk_level in ['high', 'critical'] or risk_score > 0.7
                    
                    # Extract mismatches
                    mismatches = []
                    try:
                        if isinstance(row.get('mismatches'), str):
                            mismatches = json.loads(row.get('mismatches', '[]'))
                        elif isinstance(row.get('mismatches'), list):
                            mismatches = row.get('mismatches', [])
                    except:
                        pass
                    
                    result = {
                        "influencer": influencer,
                        "product": product,
                        "followers": self.influencers.get(influencer, {}).get('followers', 0),
                        "promotion_type": "Positive Review" if not is_misleading else "Misleading Promotion",
                        "risk_level": risk_level,
                        "risk_score": risk_score,
                        "dissatisfaction": dissatisfaction,
                        "is_misleading": is_misleading,
                        "mismatches_count": len(mismatches),
                        "recommendation": self._get_recommendation(is_misleading, risk_level)
                    }
                    results.append(result)
        
        return results
    
    def _get_recommendation(self, is_misleading: bool, risk_level: str) -> str:
        """Get recommendation based on analysis."""
        if is_misleading and risk_level == 'critical':
            return "🚨 URGENT: Report to SEBI - Critical mis-selling detected"
        elif is_misleading:
            return "⚠️ WARNING: Misleading promotion detected - Monitor closely"
        else:
            return "✅ No significant issues detected"
    
    def generate_report(self, results: List[Dict], output_path: str = "reports/influencer_analysis.txt"):
        """Generate influencer analysis report."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║         INFLUENCER VS REALITY TRACKER - ANALYSIS REPORT        ║
╚═══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════════
SUMMARY
═══════════════════════════════════════════════════════════════
Total Influencers Analyzed: {len(set(r['influencer'] for r in results))}
Total Products Promoted: {len(results)}
Misleading Promotions: {sum(1 for r in results if r['is_misleading'])}

═══════════════════════════════════════════════════════════════
DETAILED ANALYSIS
═══════════════════════════════════════════════════════════════
"""
        
        for result in results:
            report += f"""
Influencer: {result['influencer']}
Followers: {result['followers']:,}
Product Promoted: {result['product']}
Promotion Type: {result['promotion_type']}
Risk Level: {result['risk_level'].upper()}
Risk Score: {result['risk_score']:.2f}/1.0
Customer Dissatisfaction: {result['dissatisfaction']:.1f}%
Mismatches Detected: {result['mismatches_count']}

Recommendation: {result['recommendation']}

{'─' * 60}
"""
        
        report += f"""
═══════════════════════════════════════════════════════════════
REGULATORY ACTIONS
═══════════════════════════════════════════════════════════════

High-risk influencers identified:
"""
        
        high_risk = [r for r in results if r['is_misleading']]
        for result in high_risk:
            report += f"  • {result['influencer']} promoting {result['product']} ({result['risk_level'].upper()})\n"
        
        report += """
Recommended Actions:
  1. Issue warning to influencers promoting high-risk products
  2. Require disclosure of financial relationships
  3. Monitor influencer content for compliance
  4. Report critical cases to regulatory authorities
  5. Educate consumers about influencer bias

═══════════════════════════════════════════════════════════════
Generated by Veritas Finance AI System
═══════════════════════════════════════════════════════════════
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


def track_influencers(gap_csv: str = "data/processed/gap_analysis.csv",
                      sentiment_csv: str = "data/processed/sentiment_analysis.csv"):
    """Main function to track influencers."""
    print("=" * 60)
    print("INFLUENCER VS REALITY TRACKER")
    print("=" * 60)
    print()
    
    # Load data
    if not os.path.exists(gap_csv):
        print(f"❌ Gap analysis file not found: {gap_csv}")
        print("💡 Run: python main_pipeline.py")
        return
    
    try:
        gap_df = pd.read_csv(gap_csv)
        sentiment_df = pd.read_csv(sentiment_csv) if os.path.exists(sentiment_csv) else pd.DataFrame()
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Analyze
    tracker = InfluencerTracker()
    results = tracker.analyze_influencer_promotions(gap_df, sentiment_df)
    
    # Generate report
    report = tracker.generate_report(results)
    
    print("✅ Analysis complete!")
    print(f"\n📊 Results:")
    print(f"   Total promotions analyzed: {len(results)}")
    print(f"   Misleading promotions: {sum(1 for r in results if r['is_misleading'])}")
    print(f"\n📄 Report saved to: reports/influencer_analysis.txt")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for result in results:
        status = "🚨 HIGH RISK" if result['is_misleading'] else "✅ OK"
        print(f"\n{result['influencer']}: {result['product']}")
        print(f"  Status: {status}")
        print(f"  Risk: {result['risk_level'].upper()} ({result['risk_score']:.2f})")
        print(f"  Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    track_influencers()
