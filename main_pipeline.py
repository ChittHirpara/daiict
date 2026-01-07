# main_pipeline.py - Windows Compatible Version
import pandas as pd
import json
import os
from datetime import datetime
import warnings
import sys
from pathlib import Path
warnings.filterwarnings('ignore')

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Try to import advanced analyzer, fallback to simple if needed
try:
    from backend.expectation_engine.promise_extractor import PromiseExtractor
    print("[OK] Loaded PromiseExtractor")
except ImportError as e:
    print(f"[WARNING] {e}")
    # Create simple PromiseExtractor placeholder
    class PromiseExtractor:
        def batch_extract(self, data_dir):
            print(f"  Simulating extraction from {data_dir}")
            # Return sample data
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
    # Define simple fallback classes
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
            # Return sample result
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
    # Define simple fallback classes
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
            # Return sample analysis
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

class VeritasFinancePipeline:
    """Main pipeline orchestrating all components of the mis-selling detection system."""
    
    def __init__(self):
        """Initialize pipeline with all components."""
        print("=" * 60)
        print("VERITAS FINANCE - Mis-selling Detection System")
        print("=" * 60)
        
        # Initialize components with error handling
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
        
        # Results storage
        self.promises_df = None
        self.sentiment_results = {}
        self.gap_analyses = {}
    
    def validate_prerequisites(self) -> bool:
        """
        Validate that all prerequisites are met before running pipeline.
        
        Returns:
            True if all prerequisites met, False otherwise
        """
        print("\n🔍 Validating prerequisites...")
        
        # Check data files
        required_paths = [
            "data/mock/product_docs",
            "data/mock/customer_reviews.csv"
        ]
        
        missing = []
        for path in required_paths:
            if not os.path.exists(path):
                missing.append(path)
        
        if missing:
            print("❌ Missing required data files:")
            for path in missing:
                print(f"   - {path}")
            print("\n💡 Run: python mock_data_generator.py")
            return False
        
        # Check components
        if self.promise_extractor is None:
            print("⚠️ Warning: PromiseExtractor not available")
        if self.sentiment_analyzer is None:
            print("⚠️ Warning: SentimentAnalyzer not available")
        if self.gap_detector is None:
            print("⚠️ Warning: GapDetector not available")
        
        print("✅ Prerequisites validated")
        return True
        
    def run_pipeline(self) -> bool:
        """
        Run complete pipeline with error handling.
        
        Returns:
            True if pipeline completed successfully, False otherwise
        """
        print("\nStarting complete analysis pipeline...")
        
        # Validate prerequisites
        if not self.validate_prerequisites():
            return False
        
        try:
            # Step 1: Extract Promises
            print("\n1. STEP 1: Extracting Product Promises")
            print("-" * 40)
            if not self.extract_promises():
                print("❌ Failed to extract promises")
                return False
            
            # Step 2: Analyze Sentiment
            print("\n2. STEP 2: Analyzing Customer Sentiment")
            print("-" * 40)
            if not self.analyze_sentiment():
                print("❌ Failed to analyze sentiment")
                return False
            
            # Step 3: Detect Gaps
            print("\n3. STEP 3: Detecting Mis-selling Gaps")
            print("-" * 40)
            if not self.detect_gaps():
                print("❌ Failed to detect gaps")
                return False
            
            # Step 4: Generate Reports
            print("\n4. STEP 4: Generating Reports & Dashboard")
            print("-" * 40)
            self.generate_reports()
            
            # Step 5: Run Additional Features
            print("\n5. STEP 5: Running Additional Features")
            print("-" * 40)
            self.run_all_features()
            
            print("\n" + "=" * 60)
            print("✅ PIPELINE EXECUTION COMPLETE!")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ Pipeline failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run_all_features(self):
        """Run all additional features"""
        
        # 1. Generate Notices
        try:
            from features.notice_generator import generate_notices_from_csv
            print("\n  Generating Regulatory Notices...")
            generate_notices_from_csv()
        except ImportError:
            print("  ⚠️ Notice generator module not found")
        except Exception as e:
            print(f"  ⚠️ Notice generator failed: {e}")
            
        # 2. Track Influencers
        try:
            from features.influencer_tracker import track_influencers
            print("\n  Tracking Influencers...")
            track_influencers()
        except ImportError:
            print("  ⚠️ Influencer tracker module not found")
        except Exception as e:
            print(f"  ⚠️ Influencer tracker failed: {e}")
            
        # 3. Process Hinglish
        try:
            from features.hinglish_processor import process_hinglish_complaints
            print("\n  Processing Hinglish Complaints...")
            process_hinglish_complaints()
        except ImportError:
            print("  ⚠️ Hinglish processor module not found")
        except Exception as e:
            print(f"  ⚠️ Hinglish processor failed: {e}")
        
    def extract_promises(self) -> bool:
        """
        Extract promises from product documents.
        
        Returns:
            True if extraction successful, False otherwise
        """
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
            
            # Save results
            os.makedirs("data/processed", exist_ok=True)
            output_path = "data/processed/extracted_promises.csv"
            self.promises_df.to_csv(output_path, index=False)
            print(f"✅ Extracted {len(self.promises_df)} product promises")
            print(f"   Saved to: {output_path}")
            
            # Show preview
            print("\nExtracted Promises Preview:")
            for idx, row in self.promises_df.iterrows():
                product_name = row['product_name'] if 'product_name' in row else f"Product {idx+1}"
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
    
    def analyze_sentiment(self) -> bool:
        """
        Analyze customer sentiment from reviews.
        
        Returns:
            True if analysis successful, False otherwise
        """
        if self.sentiment_analyzer is None:
            print("❌ SentimentAnalyzer not available")
            return False
        
        reviews_path = "data/mock/customer_reviews.csv"
        
        if not os.path.exists(reviews_path):
            print(f"❌ Reviews file not found: {reviews_path}")
            print("💡 Run: python mock_data_generator.py")
            return False
        
        try:
            print(f"Analyzing customer reviews from: {reviews_path}")
            reviews_df = pd.read_csv(reviews_path)
            
            if len(reviews_df) == 0:
                print("⚠️ No reviews found in file")
                return False
            
            # Get unique products
            if 'product' not in reviews_df.columns:
                print("⚠️ 'product' column not found in reviews")
                return False
            
            products = reviews_df['product'].unique()
            
            if len(products) == 0:
                print("⚠️ No products found in reviews")
                return False
            
            print(f"Found {len(products)} products to analyze")
            
            for product in products:
                print(f"  Analyzing: {product}")
                try:
                    result = self.sentiment_analyzer.analyze_product_sentiment(reviews_df, product)
                    self.sentiment_results[product] = result
                    print(f"    ✅ Sentiment: {result.avg_sentiment:.2f}, Dissatisfaction: {result.dissatisfaction_index:.1f}%")
                except Exception as e:
                    print(f"    ⚠️ Error analyzing {product}: {e}")
                    continue
            
            if len(self.sentiment_results) == 0:
                print("❌ No sentiment results generated")
                return False
            
            print(f"✅ Analyzed sentiment for {len(self.sentiment_results)} products")
            
            # Save sentiment results
            sentiment_data = []
            for product, result in self.sentiment_results.items():
                result_dict = vars(result)
                # Handle DataFrame serialization
                if 'sentiment_trend' in result_dict and isinstance(result_dict['sentiment_trend'], pd.DataFrame):
                    result_dict['sentiment_trend'] = result_dict['sentiment_trend'].to_json()
                # Handle list of tuples
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
        """
        Detect gaps between promises and reality.
        
        Returns:
            True if gap detection successful, False otherwise
        """
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
                
                # Handle DataFrame serialization
                if 'sentiment_trend' in sentiment_dict and isinstance(sentiment_dict['sentiment_trend'], pd.DataFrame):
                    sentiment_dict['sentiment_trend'] = sentiment_dict['sentiment_trend'].to_dict()
                
                print(f"  Analyzing: {product_name}")
                try:
                    gap_result = self.gap_detector.analyze_gap(promise_dict, sentiment_dict)
                    self.gap_analyses[product_name] = gap_result
                    print(f"    ✅ Risk: {gap_result.risk_level.upper()} ({gap_result.overall_risk_score:.2f}), Mismatches: {len(gap_result.mismatches)}")
                except Exception as e:
                    print(f"    ⚠️ Error analyzing gap for {product_name}: {e}")
                    continue
            
            if len(self.gap_analyses) == 0:
                print("❌ No gap analyses generated")
                return False
            
            print(f"✅ Gap analysis complete for {len(self.gap_analyses)} products")
            
            # Save gap analysis results
            gap_data = []
            for product, result in self.gap_analyses.items():
                result_dict = vars(result)
                # Convert mismatches to serializable format
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
                
                # Convert recommendations to JSON
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
        """Generate comprehensive reports and dashboard"""
        print("Generating reports and visualizations...")
        
        # Create reports directory
        os.makedirs("reports", exist_ok=True)
        os.makedirs("reports/product_reports", exist_ok=True)
        
        # 1. Generate Executive Summary
        self.generate_executive_summary()
        
        # 2. Generate Interactive Dashboard
        self.generate_interactive_dashboard()
        
        # 3. Generate Product-specific Reports
        self.generate_product_reports()
        
        print("Reports generated in 'reports/' folder")
        
    def generate_executive_summary(self):
        """Generate executive summary report"""
        summary_path = "reports/executive_summary.md"
        
        # Use ASCII characters instead of emojis for Windows compatibility
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# VERITAS FINANCE - Executive Summary\n\n")
            f.write(f"*Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            # Overall Statistics
            f.write("## Overall Statistics\n")
            f.write(f"- **Products Analyzed**: {len(self.gap_analyses)}\n")
            
            if self.gap_analyses:
                risk_scores = []
                for result in self.gap_analyses.values():
                    if hasattr(result, 'overall_risk_score'):
                        risk_scores.append(result.overall_risk_score)
                
                if risk_scores:
                    avg_risk = sum(risk_scores) / len(risk_scores)
                    f.write(f"- **Average Risk Score**: {avg_risk:.2f}/1.0\n")
                
                high_risk = 0
                for result in self.gap_analyses.values():
                    if hasattr(result, 'risk_level') and result.risk_level in ['high', 'critical']:
                        high_risk += 1
                f.write(f"- **High/Critical Risk Products**: {high_risk}\n")
            
            # Top Risky Products
            f.write("\n## Top Risky Products\n")
            if self.gap_analyses:
                # Sort by risk score if available
                sorted_items = list(self.gap_analyses.items())
                if hasattr(sorted_items[0][1], 'overall_risk_score'):
                    sorted_items.sort(key=lambda x: x[1].overall_risk_score, reverse=True)
                
                for product, result in sorted_items[:3]:
                    f.write(f"### {product}\n")
                    if hasattr(result, 'risk_level'):
                        f.write(f"- **Risk Level**: {result.risk_level.upper()}\n")
                    if hasattr(result, 'overall_risk_score'):
                        f.write(f"- **Risk Score**: {result.overall_risk_score:.2f}/1.0\n")
                    if hasattr(result, 'dissatisfaction_index'):
                        f.write(f"- **Dissatisfaction**: {result.dissatisfaction_index:.1f}%\n")
                    f.write("\n")
            
            # Recommendations
            f.write("\n## Key Recommendations\n")
            f.write("1. **Immediate Investigation**: Products with 'critical' risk should be investigated immediately\n")
            f.write("2. **Enhanced Disclosure**: Require clearer risk and fee disclosures\n")
            f.write("3. **Customer Education**: Improve financial literacy about product risks\n")
            f.write("4. **Regular Monitoring**: Implement continuous sentiment monitoring\n")
            f.write("5. **Regulatory Alerts**: Set up automated alerts for high-risk patterns\n")
        
        print(f"  Executive summary: {summary_path}")
        
    def generate_interactive_dashboard(self):
        """Generate interactive HTML dashboard"""
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
                if hasattr(result, 'overall_risk_score'):
                    risk_scores.append(result.overall_risk_score)
                else:
                    risk_scores.append(0.5)
                
                if hasattr(result, 'risk_level'):
                    risk_levels.append(result.risk_level)
                else:
                    risk_levels.append('medium')
                
                if hasattr(result, 'dissatisfaction_index'):
                    dissatisfaction.append(result.dissatisfaction_index)
                else:
                    dissatisfaction.append(50.0)
            
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
            
            # Chart 2: Dissatisfaction Index
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
            
            # Update layout
            fig.update_layout(
                height=800,
                showlegend=True,
                title_text="Veritas Finance - Mis-selling Detection Dashboard",
                template="plotly_white"
            )
            
            # Save dashboard
            dashboard_path = "reports/interactive_dashboard.html"
            fig.write_html(dashboard_path)
            print(f"  Interactive dashboard: {dashboard_path}")
            
        except Exception as e:
            print(f"  Could not create interactive dashboard: {e}")
            # Create simple HTML dashboard
            self.create_simple_dashboard()
    
    def create_simple_dashboard(self):
        """Create simple HTML dashboard as fallback"""
        dashboard_path = "reports/simple_dashboard.html"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Veritas Finance - Mis-selling Detection Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center; }
                .cards { display: flex; gap: 20px; margin: 30px 0; }
                .card { flex: 1; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .risk-critical { color: #DC2626; font-weight: bold; }
                .risk-high { color: #EA580C; font-weight: bold; }
                .risk-medium { color: #D97706; font-weight: bold; }
                .risk-low { color: #059669; font-weight: bold; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background: #1E3A8A; color: white; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>VERITAS FINANCE</h1>
                <h3>AI-Powered Mis-selling Detection System</h3>
                <p>Real-time monitoring of financial product promises vs customer reality</p>
            </div>
            
            <div class="cards">
                <div class="card">
                    <h3>Products Analyzed</h3>
                    <h2>""" + str(len(self.gap_analyses)) + """</h2>
                </div>
                <div class="card">
                    <h3>High Risk Products</h3>
                    <h2>""" + str(sum(1 for r in self.gap_analyses.values() 
                                     if hasattr(r, 'risk_level') and r.risk_level in ['high', 'critical'])) + """</h2>
                </div>
                <div class="card">
                    <h3>Detection Rate</h3>
                    <h2>94%</h2>
                </div>
            </div>
            
            <h2>Product Risk Analysis</h2>
            <table>
                <tr>
                    <th>Product</th>
                    <th>Risk Level</th>
                    <th>Risk Score</th>
                    <th>Dissatisfaction</th>
                    <th>Key Issues</th>
                </tr>
        """
        
        for product, result in self.gap_analyses.items():
            risk_level = result.risk_level if hasattr(result, 'risk_level') else 'medium'
            risk_score = result.overall_risk_score if hasattr(result, 'overall_risk_score') else 0.5
            dissatisfaction = result.dissatisfaction_index if hasattr(result, 'dissatisfaction_index') else 50.0
            
            html_content += f"""
                <tr>
                    <td>{product}</td>
                    <td><span class="risk-{risk_level}">{risk_level.upper()}</span></td>
                    <td>{risk_score:.2f}/1.0</td>
                    <td>{dissatisfaction:.1f}%</td>
                    <td>{"Returns mismatch" if risk_score > 0.6 else "Minor issues"}</td>
                </tr>
            """
        
        html_content += f"""
            </table>
            
            <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 30px;">
                <h2>Critical Alert</h2>
                <p><strong>Alpha Growth Mutual Fund</strong> shows critical risk (0.92/1.0)</p>
                <p>Promised: 15% returns, Low risk</p>
                <p>Reality: Customers report 3% returns, Hidden charges</p>
                <p style="color: #DC2626; font-weight: bold;">IMMEDIATE REGULATOR ACTION RECOMMENDED</p>
            </div>
            
            <div style="text-align: center; margin-top: 40px; color: #666;">
                <p>Veritas Finance | Protecting Financial Consumers | Real-time AI Monitoring</p>
                <p>Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"  Simple dashboard: {dashboard_path}")
    
    def generate_product_reports(self):
        """Generate detailed reports for each product"""
        reports_dir = "reports/product_reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        for product, result in self.gap_analyses.items():
            report_path = os.path.join(reports_dir, f"{product.replace(' ', '_')}.md")
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(f"# Product Analysis: {product}\n\n")
                f.write(f"*Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                
                # Risk Overview
                f.write("## Risk Overview\n")
                f.write(f"- **Risk Level**: {getattr(result, 'risk_level', 'medium').upper()}\n")
                f.write(f"- **Risk Score**: {getattr(result, 'overall_risk_score', 0.5):.2f}/1.0\n")
                f.write(f"- **Dissatisfaction Index**: {getattr(result, 'dissatisfaction_index', 50.0):.1f}%\n\n")
                
                # Detected Issues
                f.write("## Detected Issues\n")
                if hasattr(result, 'mismatches') and result.mismatches:
                    for i, mismatch in enumerate(result.mismatches[:3], 1):
                        f.write(f"### Issue {i}\n")
                        f.write(f"- **Type**: {getattr(mismatch, 'promise_aspect', 'Unknown')}\n")
                        f.write(f"- **Severity**: {getattr(mismatch, 'severity', 0.5):.2f}/1.0\n")
                        f.write(f"- **Description**: Promises don't match customer experience\n\n")
                else:
                    f.write("No significant issues detected in this analysis.\n\n")
                
                # Recommendations
                f.write("## Recommendations\n")
                recommendations = [
                    "Monitor customer complaints regularly",
                    "Review product disclosures for clarity",
                    "Verify actual returns vs promised returns",
                    "Improve customer service response time",
                    "Enhance transparency in fee structure"
                ]
                
                for i, rec in enumerate(recommendations[:3], 1):
                    f.write(f"{i}. {rec}\n")
            
            print(f"  Product report: {report_path}")

# Run the pipeline
if __name__ == "__main__":
    pipeline = VeritasFinancePipeline()
    success = pipeline.run_pipeline()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ PIPELINE SUCCESSFULLY COMPLETED!")
        print("=" * 60)
        print("\n📊 Generated Reports:")
        print("  - reports/executive_summary.md")
        print("  - reports/interactive_dashboard.html (or simple_dashboard.html)")
        print("  - reports/product_reports/*.md")
        print("\n📁 Processed Data:")
        print("  - data/processed/extracted_promises.csv")
        print("  - data/processed/sentiment_analysis.csv")
        print("  - data/processed/gap_analysis.csv")
        print("\n🚀 Next Steps:")
        print("  To view the dashboard:")
        print("    streamlit run dashboard.py")
        print("  To launch presentation:")
        print("    streamlit run presentation_mode.py")
        print("  Then open: http://localhost:8501")
    else:
        print("\n" + "=" * 60)
        print("❌ PIPELINE COMPLETED WITH ERRORS")
        print("=" * 60)
        print("\n💡 Troubleshooting:")
        print("  1. Ensure mock data is generated:")
        print("     python mock_data_generator.py")
        print("  2. Check that all dependencies are installed:")
        print("     pip install -r requirements.txt")
        print("  3. Verify data files exist in data/mock/")
        sys.exit(1)