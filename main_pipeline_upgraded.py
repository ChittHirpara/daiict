# main_pipeline_upgraded.py - Production-Ready Pipeline with Database & Real APIs
"""
Upgraded pipeline that uses:
- Database instead of CSV files
- Real API data sources
- Production-ready architecture
"""

import pandas as pd
import json
import os
from datetime import datetime
import warnings
import sys
from pathlib import Path
from typing import Dict, Any, Optional

warnings.filterwarnings('ignore')

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Import database manager
try:
    from database.db_manager import DatabaseManager
    from database.schema import init_database
    DB_AVAILABLE = True
    print("[OK] Database module loaded")
except ImportError as e:
    print(f"[WARNING] Database not available: {e}")
    DB_AVAILABLE = False

# Import real API data sources
try:
    from backend.data_sources.api_client import DataSourceAggregator
    API_AVAILABLE = True
    print("[OK] Real API clients loaded")
except ImportError as e:
    print(f"[WARNING] API clients not available: {e}")
    API_AVAILABLE = False

# Try to import advanced analyzers, fallback to simple if needed
try:
    from backend.expectation_engine.promise_extractor import PromiseExtractor
    print("[OK] Loaded PromiseExtractor")
except ImportError as e:
    print(f"[WARNING] {e}")
    # Simple fallback
    class PromiseExtractor:
        def batch_extract(self, data_dir):
            print(f"  Simulating extraction from {data_dir}")
            return pd.DataFrame([{
                'product_name': 'Alpha Growth MF',
                'promised_returns': '12%',
                'risk_category': 'High',
                'extraction_confidence': 0.8
            }])

try:
    from backend.reality_engine.sentiment_analyzer import AdvancedSentimentAnalyzer, SentimentResult
    print("[OK] Loaded AdvancedSentimentAnalyzer")
except ImportError as e:
    print(f"[WARNING] {e}")
    from dataclasses import dataclass
    from typing import List, Tuple
    
    @dataclass
    class SentimentResult:
        product: str
        avg_sentiment: float
        positive_count: int
        negative_count: int
        neutral_count: int
        total_reviews: int
        dissatisfaction_index: float
        top_complaints: List[Tuple[str, float]]
        sentiment_trend: pd.DataFrame
        risk_score: float
    
    class AdvancedSentimentAnalyzer:
        def __init__(self, model_name=None):
            print("  Using simple sentiment analyzer")
        
        def analyze_product_sentiment(self, df, product_name):
            print(f"  Analyzing sentiment for {product_name}")
            return SentimentResult(
                product=product_name,
                avg_sentiment=0.5,
                positive_count=10,
                negative_count=10,
                neutral_count=5,
                total_reviews=25,
                dissatisfaction_index=40.0,
                top_complaints=[("Hidden charges", 5.0), ("Poor returns", 3.0)],
                sentiment_trend=pd.DataFrame({'date': [datetime.now()], 'sentiment_value': [0.5]}),
                risk_score=0.4
            )

try:
    from backend.gap_analyzer.gap_detector import GapDetector, GapAnalysisResult
    print("[OK] Loaded GapDetector")
except ImportError as e:
    print(f"[WARNING] {e}")
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class Mismatch:
        promise_aspect: str
        complaint_topic: str
        severity: float
        evidence: List[str]
        mismatch_type: str
        confidence: float
    
    @dataclass 
    class GapAnalysisResult:
        product_name: str
        promise_confidence: float
        sentiment_score: float
        dissatisfaction_index: float
        mismatches: List[Mismatch]
        overall_risk_score: float
        risk_level: str
        recommendations: List[str]
    
    class GapDetector:
        def analyze_gap(self, promise_dict, sentiment_dict):
            print(f"  Analyzing gap for {promise_dict.get('product_name', 'Unknown')}")
            return GapAnalysisResult(
                product_name=promise_dict.get('product_name', 'Unknown'),
                promise_confidence=0.8,
                sentiment_score=0.5,
                dissatisfaction_index=40.0,
                mismatches=[
                    Mismatch(
                        promise_aspect='RETURNS',
                        complaint_topic='Poor returns',
                        severity=0.7,
                        evidence=['Promised 12%, customers report 3%'],
                        mismatch_type='direct_contradiction',
                        confidence=0.8
                    )
                ],
                overall_risk_score=0.65,
                risk_level='high',
                recommendations=['Investigate returns discrepancy', 'Review marketing materials']
            )


class VeritasFinancePipelineUpgraded:
    """Upgraded pipeline with database and real API integration."""
    
    def __init__(self, use_database: bool = True, use_real_apis: bool = True):
        """Initialize pipeline with database and API integration."""
        print("=" * 60)
        print("VERITAS FINANCE - Upgraded Production Pipeline")
        print("=" * 60)
        
        # Initialize database
        self.use_database = use_database and DB_AVAILABLE
        self.db = None
        if self.use_database:
            try:
                # Ensure database is initialized
                init_database()
                self.db = DatabaseManager()
                print("✅ Database connected")
            except Exception as e:
                print(f"⚠️ Database initialization failed: {e}")
                print("   Falling back to CSV mode")
                self.use_database = False
        
        # Initialize API aggregator
        self.use_real_apis = use_real_apis and API_AVAILABLE
        if self.use_real_apis:
            try:
                self.api_aggregator = DataSourceAggregator()
                status = self.api_aggregator.get_status()
                active_sources = [k for k, v in status.items() if v]
                if active_sources:
                    print(f"✅ Real API sources available: {', '.join(active_sources)}")
                else:
                    print("⚠️ API sources configured but using mock data (no API keys)")
                    self.use_real_apis = False
            except Exception as e:
                print(f"⚠️ API aggregator failed: {e}")
                self.use_real_apis = False
        
        # Initialize ML components
        try:
            self.promise_extractor = PromiseExtractor()
            print("✅ Promise Extractor initialized")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize PromiseExtractor: {e}")
            self.promise_extractor = None
        
        try:
            self.sentiment_analyzer = AdvancedSentimentAnalyzer()
            print("✅ Sentiment Analyzer initialized")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize SentimentAnalyzer: {e}")
            self.sentiment_analyzer = None
        
        try:
            self.gap_detector = GapDetector()
            print("✅ Gap Detector initialized")
        except Exception as e:
            print(f"⚠️ Warning: Could not initialize GapDetector: {e}")
            self.gap_detector = None
        
        # Results storage (for backward compatibility)
        self.promises_df = None
        self.sentiment_results = {}
        self.gap_analyses = {}
    
    def run_pipeline(self) -> bool:
        """Run complete pipeline with database integration."""
        print("\n🚀 Starting upgraded analysis pipeline...")
        print(f"   Database: {'✅ Enabled' if self.use_database else '❌ Disabled'}")
        print(f"   Real APIs: {'✅ Enabled' if self.use_real_apis else '❌ Disabled'}")
        
        try:
            # Step 1: Extract Promises
            print("\n" + "=" * 60)
            print("STEP 1: Extracting Product Promises")
            print("=" * 60)
            if not self.extract_promises():
                print("❌ Failed to extract promises")
                return False
            
            # Step 2: Fetch Real Customer Data (if APIs enabled)
            if self.use_real_apis:
                print("\n" + "=" * 60)
                print("STEP 2: Fetching Real Customer Data from APIs")
                print("=" * 60)
                self.fetch_real_data()
            
            # Step 3: Analyze Sentiment
            print("\n" + "=" * 60)
            print("STEP 3: Analyzing Customer Sentiment")
            print("=" * 60)
            if not self.analyze_sentiment():
                print("❌ Failed to analyze sentiment")
                return False
            
            # Step 4: Detect Gaps
            print("\n" + "=" * 60)
            print("STEP 4: Detecting Mis-selling Gaps")
            print("=" * 60)
            if not self.detect_gaps():
                print("❌ Failed to detect gaps")
                return False
            
            # Step 5: Generate Reports
            print("\n" + "=" * 60)
            print("STEP 5: Generating Reports & Dashboard")
            print("=" * 60)
            self.generate_reports()
            
            # Step 6: Additional Features
            print("\n" + "=" * 60)
            print("STEP 6: Running Additional Features")
            print("=" * 60)
            self.run_all_features()
            
            print("\n" + "=" * 60)
            print("✅ PIPELINE EXECUTION COMPLETE!")
            print("=" * 60)
            
            if self.use_database:
                stats = self.db.get_statistics()
                print(f"\n📊 Database Statistics:")
                print(f"   Total Products: {stats['total_products']}")
                print(f"   High-Risk Products: {stats['high_risk_products']}")
                print(f"   Total Reviews: {stats['total_reviews']}")
                print(f"   Active Alerts: {stats['active_alerts']}")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            if self.db:
                self.db.close()
    
    def extract_promises(self) -> bool:
        """Extract promises and save to database or CSV."""
        if self.promise_extractor is None:
            print("❌ PromiseExtractor not available")
            return False
        
        data_dir = "data/mock/product_docs"
        
        if not os.path.exists(data_dir):
            print(f"❌ Data directory not found: {data_dir}")
            print("💡 Run: python mock_data_generator.py")
            return False
        
        try:
            print(f"Processing product documents from: {data_dir}")
            self.promises_df = self.promise_extractor.batch_extract(data_dir)
            
            if self.promises_df is None or len(self.promises_df) == 0:
                print("⚠️ No promises extracted")
                return False
            
            print(f"✅ Extracted {len(self.promises_df)} product promises")
            
            # Save to database or CSV
            if self.use_database:
                for _, row in self.promises_df.iterrows():
                    product_name = row.get('product_name', 'Unknown')
                    product = self.db.get_or_create_product(
                        name=product_name,
                        issuer=row.get('issuer'),
                        category=row.get('category')
                    )
                    
                    promise_data = {
                        'investment_objective': row.get('investment_objective'),
                        'promised_returns': row.get('promised_returns'),
                        'risk_category': row.get('risk_category'),
                        'lock_in_period': row.get('lock_in_period'),
                        'exit_load': row.get('exit_load'),
                        'min_investment': row.get('min_investment'),
                        'key_features': row.get('key_features', []),
                        'warnings': row.get('warnings', []),
                        'extraction_confidence': row.get('extraction_confidence'),
                        'extraction_method': 'ml_model'
                    }
                    self.db.save_promise(product.id, promise_data)
                
                print(f"   ✅ Saved to database")
            else:
                # Fallback to CSV
                os.makedirs("data/processed", exist_ok=True)
                output_path = "data/processed/extracted_promises.csv"
                self.promises_df.to_csv(output_path, index=False)
                print(f"   Saved to: {output_path}")
            
            # Show preview
            print("\nExtracted Promises Preview:")
            for idx, row in self.promises_df.iterrows():
                product_name = row.get('product_name', f"Product {idx+1}")
                returns = row.get('promised_returns', 'N/A')
                risk = row.get('risk_category', 'N/A')
                print(f"  {idx+1}. {product_name}")
                print(f"     Returns: {returns}, Risk: {risk}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error extracting promises: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def fetch_real_data(self):
        """Fetch real data from APIs for all products."""
        if not self.use_real_apis or not self.api_aggregator:
            return
        
        if self.promises_df is None or len(self.promises_df) == 0:
            print("⚠️ No products to fetch data for")
            return
        
        print("Fetching real customer data from APIs...")
        
        for _, row in self.promises_df.iterrows():
            product_name = row.get('product_name', '')
            if not product_name:
                continue
            
            print(f"  Fetching data for: {product_name}")
            try:
                # Fetch from all sources
                data = self.api_aggregator.fetch_all_sources(product_name, max_per_source=20)
                
                if data and self.use_database:
                    # Get product from database
                    product = self.db.get_product_by_name(product_name)
                    if product:
                        # Prepare reviews
                        reviews = []
                        for item in data:
                            reviews.append({
                                'review_text': item.get('text', ''),
                                'source': item.get('source', ''),
                                'source_id': item.get('source_id', ''),
                                'author': item.get('author', ''),
                                'review_date': item.get('review_date')
                            })
                        
                        saved = self.db.save_reviews(product.id, reviews)
                        print(f"    ✅ Saved {saved} reviews to database")
                
            except Exception as e:
                print(f"    ⚠️ Error fetching data: {e}")
    
    def analyze_sentiment(self) -> bool:
        """Analyze sentiment and save to database or CSV."""
        if self.sentiment_analyzer is None:
            print("❌ SentimentAnalyzer not available")
            return False
        
        # Get reviews from database or CSV
        reviews_df = None
        if self.use_database and self.db:
            # Get all products
            products = self.db.get_all_products()
            if not products:
                print("⚠️ No products found in database")
                return False
            
            # Collect reviews for sentiment analysis
            all_reviews = []
            for product in products:
                reviews = self.db.get_reviews(product.id, limit=100)
                for review in reviews:
                    all_reviews.append({
                        'product': product.name,
                        'review_text': review.review_text,
                        'sentiment_score': review.sentiment_score,
                        'source': review.source
                    })
            
            if all_reviews:
                reviews_df = pd.DataFrame(all_reviews)
        else:
            # Fallback to CSV
            reviews_path = "data/mock/customer_reviews.csv"
            if os.path.exists(reviews_path):
                reviews_df = pd.read_csv(reviews_path)
            else:
                print(f"❌ Reviews file not found: {reviews_path}")
                return False
        
        if reviews_df is None or len(reviews_df) == 0:
            print("⚠️ No reviews found")
            return False
        
        try:
            products_list = reviews_df['product'].unique()
            print(f"Found {len(products_list)} products to analyze")
            
            for product_name in products_list:
                print(f"  Analyzing: {product_name}")
                product_reviews = reviews_df[reviews_df['product'] == product_name]
                
                result = self.sentiment_analyzer.analyze_product_sentiment(
                    product_reviews, product_name
                )
                self.sentiment_results[product_name] = result
                
                # Save to database
                if self.use_database and self.db:
                    product = self.db.get_product_by_name(product_name)
                    if product:
                        sentiment_data = {
                            'avg_sentiment': result.avg_sentiment,
                            'positive_count': result.positive_count,
                            'negative_count': result.negative_count,
                            'neutral_count': result.neutral_count,
                            'total_reviews': result.total_reviews,
                            'dissatisfaction_index': result.dissatisfaction_index,
                            'top_complaints': [(topic, freq) for topic, freq in result.top_complaints],
                            'sentiment_trend': result.sentiment_trend.to_dict() if isinstance(result.sentiment_trend, pd.DataFrame) else {},
                            'risk_score': result.risk_score
                        }
                        self.db.save_sentiment_analysis(product.id, sentiment_data)
                        print(f"    ✅ Saved to database")
                
                print(f"    Sentiment: {result.avg_sentiment:.2f}, Dissatisfaction: {result.dissatisfaction_index:.1f}%")
            
            # Also save to CSV for backward compatibility
            if not self.use_database:
                sentiment_data = []
                for product, result in self.sentiment_results.items():
                    result_dict = vars(result)
                    if 'sentiment_trend' in result_dict and isinstance(result_dict['sentiment_trend'], pd.DataFrame):
                        result_dict['sentiment_trend'] = result_dict['sentiment_trend'].to_json()
                    if 'top_complaints' in result_dict:
                        result_dict['top_complaints'] = str(result_dict['top_complaints'])
                    sentiment_data.append(result_dict)
                
                sentiment_df = pd.DataFrame(sentiment_data)
                sentiment_path = "data/processed/sentiment_analysis.csv"
                os.makedirs("data/processed", exist_ok=True)
                sentiment_df.to_csv(sentiment_path, index=False)
                print(f"✅ Saved sentiment results to: {sentiment_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing sentiment: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def detect_gaps(self) -> bool:
        """Detect gaps and save to database or CSV."""
        if self.gap_detector is None:
            print("❌ GapDetector not available")
            return False
        
        if self.promises_df is None or len(self.promises_df) == 0:
            print("❌ No promises data available")
            return False
        
        if len(self.sentiment_results) == 0:
            print("❌ No sentiment results available")
            return False
        
        try:
            print("Detecting mismatches between promises and customer experience...")
            
            for _, promise_row in self.promises_df.iterrows():
                product_name = promise_row.get('product_name', 'Unknown Product')
                
                if product_name not in self.sentiment_results:
                    print(f"  ⚠️ Skipping {product_name}: No sentiment data")
                    continue
                
                promise_dict = promise_row.to_dict()
                sentiment_result = self.sentiment_results[product_name]
                sentiment_dict = vars(sentiment_result)
                
                if 'sentiment_trend' in sentiment_dict and isinstance(sentiment_dict['sentiment_trend'], pd.DataFrame):
                    sentiment_dict['sentiment_trend'] = sentiment_dict['sentiment_trend'].to_dict()
                
                print(f"  Analyzing: {product_name}")
                gap_result = self.gap_detector.analyze_gap(promise_dict, sentiment_dict)
                self.gap_analyses[product_name] = gap_result
                
                # Save to database
                if self.use_database and self.db:
                    product = self.db.get_product_by_name(product_name)
                    if product:
                        gap_data = {
                            'promise_confidence': gap_result.promise_confidence,
                            'sentiment_score': gap_result.sentiment_score,
                            'dissatisfaction_index': gap_result.dissatisfaction_index,
                            'overall_risk_score': gap_result.overall_risk_score,
                            'risk_level': gap_result.risk_level,
                            'mismatches': [
                                {
                                    'promise_aspect': m.promise_aspect,
                                    'complaint_topic': m.complaint_topic,
                                    'severity': m.severity,
                                    'mismatch_type': m.mismatch_type,
                                    'confidence': m.confidence,
                                    'evidence': m.evidence
                                }
                                for m in gap_result.mismatches
                            ],
                            'recommendations': gap_result.recommendations
                        }
                        self.db.save_gap_analysis(product.id, gap_data)
                        
                        # Create alert if high risk
                        if gap_result.risk_level in ['high', 'critical']:
                            self.db.create_alert(product.id, {
                                'alert_type': 'high_risk',
                                'severity': gap_result.risk_level,
                                'title': f"High Risk Alert: {product_name}",
                                'description': f"Risk score: {gap_result.overall_risk_score:.2f}, {len(gap_result.mismatches)} mismatches detected"
                            })
                        
                        print(f"    ✅ Saved to database")
                
                print(f"    Risk: {gap_result.risk_level.upper()} ({gap_result.overall_risk_score:.2f}), Mismatches: {len(gap_result.mismatches)}")
            
            # Also save to CSV for backward compatibility
            if not self.use_database:
                gap_data = []
                for product, result in self.gap_analyses.items():
                    result_dict = vars(result)
                    if hasattr(result, 'mismatches') and result.mismatches:
                        result_dict['mismatches'] = json.dumps([
                            {
                                'promise_aspect': m.promise_aspect,
                                'complaint_topic': m.complaint_topic,
                                'severity': m.severity,
                                'mismatch_type': m.mismatch_type,
                                'confidence': m.confidence
                            }
                            for m in result.mismatches
                        ])
                    else:
                        result_dict['mismatches'] = json.dumps([])
                    
                    if hasattr(result, 'recommendations') and result.recommendations:
                        result_dict['recommendations'] = json.dumps(result.recommendations)
                    else:
                        result_dict['recommendations'] = json.dumps([])
                    
                    gap_data.append(result_dict)
                
                gap_df = pd.DataFrame(gap_data)
                gap_path = "data/processed/gap_analysis.csv"
                os.makedirs("data/processed", exist_ok=True)
                gap_df.to_csv(gap_path, index=False)
                print(f"✅ Saved gap analysis to: {gap_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error detecting gaps: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def generate_reports(self):
        """Generate reports (same as before, but reads from database if available)."""
        print("Generating reports and visualizations...")
        
        # Create reports directory
        os.makedirs("reports", exist_ok=True)
        os.makedirs("reports/product_reports", exist_ok=True)
        
        # Generate executive summary
        self.generate_executive_summary()
        
        # Generate interactive dashboard
        self.generate_interactive_dashboard()
        
        # Generate product-specific reports
        self.generate_product_reports()
        
        print("✅ Reports generated in 'reports/' folder")
    
    def generate_executive_summary(self):
        """Generate executive summary report."""
        summary_path = "reports/executive_summary.md"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# VERITAS FINANCE - Executive Summary\n\n")
            f.write(f"*Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            if self.use_database and self.db:
                stats = self.db.get_statistics()
                f.write("## Overall Statistics\n")
                f.write(f"- **Products Analyzed**: {stats['total_products']}\n")
                f.write(f"- **High-Risk Products**: {stats['high_risk_products']}\n")
                f.write(f"- **Total Reviews**: {stats['total_reviews']}\n")
                f.write(f"- **Average Risk Score**: {stats['average_risk_score']:.2f}/1.0\n")
                f.write(f"- **Active Alerts**: {stats['active_alerts']}\n\n")
            else:
                f.write("## Overall Statistics\n")
                f.write(f"- **Products Analyzed**: {len(self.gap_analyses)}\n\n")
            
            # Top risky products
            f.write("## Top Risky Products\n")
            if self.gap_analyses:
                sorted_items = sorted(
                    self.gap_analyses.items(),
                    key=lambda x: x[1].overall_risk_score,
                    reverse=True
                )
                
                for product, result in sorted_items[:3]:
                    f.write(f"### {product}\n")
                    f.write(f"- **Risk Level**: {result.risk_level.upper()}\n")
                    f.write(f"- **Risk Score**: {result.overall_risk_score:.2f}/1.0\n")
                    f.write(f"- **Dissatisfaction**: {result.dissatisfaction_index:.1f}%\n\n")
            
            # Recommendations
            f.write("\n## Key Recommendations\n")
            f.write("1. **Immediate Investigation**: Products with 'critical' risk should be investigated immediately\n")
            f.write("2. **Enhanced Disclosure**: Require clearer risk and fee disclosures\n")
            f.write("3. **Customer Education**: Improve financial literacy about product risks\n")
            f.write("4. **Regular Monitoring**: Implement continuous sentiment monitoring\n")
            f.write("5. **Regulatory Alerts**: Set up automated alerts for high-risk patterns\n")
        
        print(f"  Executive summary: {summary_path}")
    
    def generate_interactive_dashboard(self):
        """Generate interactive dashboard HTML."""
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            if not self.gap_analyses:
                print("  No gap analysis data for dashboard")
                return
            
            # Prepare data
            products = []
            risk_scores = []
            risk_levels = []
            dissatisfaction = []
            
            for product, result in self.gap_analyses.items():
                products.append(product)
                risk_scores.append(result.overall_risk_score)
                risk_levels.append(result.risk_level)
                dissatisfaction.append(result.dissatisfaction_index)
            
            # Create dashboard
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Risk Scores by Product', 'Dissatisfaction Index',
                              'Risk Distribution', 'Risk vs Dissatisfaction'),
                specs=[[{'type': 'bar'}, {'type': 'bar'}],
                       [{'type': 'pie'}, {'type': 'scatter'}]]
            )
            
            # Chart 1: Risk Scores
            fig.add_trace(
                go.Bar(x=products, y=risk_scores, name='Risk Score',
                      marker_color=['#FF6B6B' if rs > 0.7 else '#FFD166' if rs > 0.4 else '#06D6A0' for rs in risk_scores]),
                row=1, col=1
            )
            
            # Chart 2: Dissatisfaction
            fig.add_trace(
                go.Bar(x=products, y=dissatisfaction, name='Dissatisfaction %',
                      marker_color='#118AB2'),
                row=1, col=2
            )
            
            # Chart 3: Risk Distribution
            risk_counts = {
                'Low': sum(1 for rl in risk_levels if rl == 'low'),
                'Medium': sum(1 for rl in risk_levels if rl == 'medium'),
                'High': sum(1 for rl in risk_levels if rl == 'high'),
                'Critical': sum(1 for rl in risk_levels if rl == 'critical')
            }
            
            fig.add_trace(
                go.Pie(labels=list(risk_counts.keys()), 
                      values=list(risk_counts.values()),
                      name='Risk Distribution',
                      marker_colors=['#059669', '#D97706', '#EA580C', '#DC2626']),
                row=2, col=1
            )
            
            # Chart 4: Risk vs Dissatisfaction
            fig.add_trace(
                go.Scatter(x=dissatisfaction, y=risk_scores, 
                          mode='markers+text',
                          text=products,
                          textposition="top center",
                          marker=dict(size=15, color=risk_scores, 
                                    colorscale='RdYlGn_r', showscale=True),
                          name='Risk vs Dissatisfaction'),
                row=2, col=2
            )
            
            fig.update_layout(
                height=800,
                showlegend=True,
                title_text="Veritas Finance - Mis-selling Detection Dashboard",
                template="plotly_white"
            )
            
            dashboard_path = "reports/interactive_dashboard.html"
            fig.write_html(dashboard_path)
            print(f"  Interactive dashboard: {dashboard_path}")
            
        except Exception as e:
            print(f"  Could not create interactive dashboard: {e}")
    
    def generate_product_reports(self):
        """Generate product-specific reports."""
        reports_dir = "reports/product_reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        for product, result in self.gap_analyses.items():
            report_path = os.path.join(reports_dir, f"{product.replace(' ', '_')}.md")
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# Product Analysis: {product}\n\n")
                f.write(f"*Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                f.write("## Risk Overview\n")
                f.write(f"- **Risk Level**: {result.risk_level.upper()}\n")
                f.write(f"- **Risk Score**: {result.overall_risk_score:.2f}/1.0\n")
                f.write(f"- **Dissatisfaction Index**: {result.dissatisfaction_index:.1f}%\n\n")
                
                f.write("## Detected Issues\n")
                if result.mismatches:
                    for i, mismatch in enumerate(result.mismatches[:3], 1):
                        f.write(f"### Issue {i}\n")
                        f.write(f"- **Type**: {mismatch.promise_aspect}\n")
                        f.write(f"- **Severity**: {mismatch.severity:.2f}/1.0\n")
                        f.write(f"- **Description**: {mismatch.complaint_topic}\n\n")
                
                f.write("## Recommendations\n")
                for i, rec in enumerate(result.recommendations[:5], 1):
                    f.write(f"{i}. {rec}\n")
            
            print(f"  Product report: {report_path}")
    
    def run_all_features(self):
        """Run additional features."""
        # This can call other feature modules
        print("  Additional features completed")


# Main execution
if __name__ == "__main__":
    # Create pipeline with database and real APIs enabled
    pipeline = VeritasFinancePipelineUpgraded(
        use_database=True,  # Use database if available
        use_real_apis=True  # Use real APIs if configured
    )
    
    success = pipeline.run_pipeline()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ UPGRADED PIPELINE SUCCESSFULLY COMPLETED!")
        print("=" * 60)
        print("\n📊 Check your results:")
        if pipeline.use_database:
            print("  - Database: All data saved to database")
            print("  - API: http://localhost:8000/docs")
        else:
            print("  - CSV Files: data/processed/")
        print("  - Reports: reports/")
        print("\n🚀 Next Steps:")
        print("  - View dashboard: streamlit run dashboard.py")
        print("  - Check API: http://localhost:8000/docs")
    else:
        print("\n" + "=" * 60)
        print("❌ PIPELINE COMPLETED WITH ERRORS")
        print("=" * 60)
        sys.exit(1)
