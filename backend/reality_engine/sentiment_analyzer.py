# backend/reality_engine/sentiment_analyzer.py - ADVANCED VERSION
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import plotly.express as px
from datetime import datetime, timedelta
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
import warnings
warnings.filterwarnings('ignore')
import os

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
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        print("Loading sentiment model... (this may take a minute)")
        try:
            # Load pre-trained sentiment model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=model_name,
                tokenizer=model_name
            )
        except Exception as e:
            print(f"⚠️ Could not load transformer model: {e}")
            print("⚠️ Using fallback sentiment analyzer...")
            self.sentiment_pipeline = None
        
        # Initialize topic model
        self.topic_model = None
        print("Loading embedding model...")
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            print("⚠️ Using simple embedding fallback")
            self.embedding_model = None
        
        # Financial-specific keywords for complaint detection
        self.financial_keywords = {
            'hidden_charges': ['hidden charge', 'hidden fee', 'undisclosed cost', 'extra charge'],
            'poor_returns': ['poor return', 'low return', 'bad return', 'not getting returns'],
            'misleading': ['mislead', 'false promise', 'lied', 'fake promise'],
            'service_issues': ['bad service', 'poor service', 'no response', 'ignore'],
            'difficult_exit': ['cannot exit', 'exit problem', 'withdrawal issue', 'lock in'],
            'agent_problem': ['agent fraud', 'agent cheat', 'bad agent', 'mis-selling']
        }
        print("✅ Sentiment analyzer ready!")
    
    def simple_analyze_sentiment(self, text: str) -> Dict:
        """Simple sentiment analysis fallback"""
        text_lower = str(text).lower()
        
        # Simple keyword-based sentiment
        positive_words = ['good', 'great', 'excellent', 'happy', 'satisfied', 'recommend']
        negative_words = ['bad', 'poor', 'terrible', 'avoid', 'worst', 'cheat', 'fraud']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return {'label': 'POSITIVE', 'score': 0.8, 'sentiment_value': 0.8}
        elif neg_count > pos_count:
            return {'label': 'NEGATIVE', 'score': 0.8, 'sentiment_value': 0.2}
        else:
            return {'label': 'NEUTRAL', 'score': 0.5, 'sentiment_value': 0.5}
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of a single text"""
        try:
            if self.sentiment_pipeline is None:
                return self.simple_analyze_sentiment(text)
            
            # Truncate to model limit
            truncated_text = text[:512] if len(text) > 512 else text
            result = self.sentiment_pipeline(truncated_text)[0]
            return {
                'label': result['label'],
                'score': result['score'],
                'sentiment_value': 1.0 if result['label'] == 'POSITIVE' else 0.0
            }
        except Exception as e:
            print(f"Warning in sentiment analysis: {e}")
            return self.simple_analyze_sentiment(text)
    
    def batch_analyze(self, df: pd.DataFrame, text_column: str = 'text') -> pd.DataFrame:
        """Analyze sentiment for batch of texts"""
        print(f"Analyzing sentiment for {len(df)} texts...")
        
        df = df.copy()
        sentiments = []
        
        for idx, text in enumerate(df[text_column]):
            sentiment = self.analyze_sentiment(str(text))
            sentiments.append(sentiment)
            
            # Progress indicator
            if (idx + 1) % 50 == 0:
                print(f"  Processed {idx + 1}/{len(df)} texts...")
        
        df['sentiment_label'] = [s['label'] for s in sentiments]
        df['sentiment_score'] = [s['score'] for s in sentiments]
        df['sentiment_value'] = [s['sentiment_value'] for s in sentiments]
        
        return df
    
    def calculate_dissatisfaction_index(self, df: pd.DataFrame, product_col: str = 'product') -> Dict:
        """Calculate dissatisfaction index per product"""
        results = {}
        
        for product in df[product_col].unique():
            product_df = df[df[product_col] == product]
            total = len(product_df)
            
            if total == 0:
                continue
            
            negative = len(product_df[product_df['sentiment_label'] == 'NEGATIVE'])
            positive = len(product_df[product_df['sentiment_label'] == 'POSITIVE'])
            neutral = total - positive - negative
            
            dissatisfaction = (negative / total) * 100 if total > 0 else 0
            
            results[product] = {
                'total_reviews': total,
                'positive_count': positive,
                'negative_count': negative,
                'neutral_count': neutral,
                'dissatisfaction_index': dissatisfaction,
                'avg_sentiment': product_df['sentiment_value'].mean()
            }
        
        return results
    
    def detect_complaint_topics(self, df: pd.DataFrame, n_topics: int = 5) -> List:
        """Detect main complaint topics using BERTopic or simple method"""
        # Filter negative reviews
        negative_reviews = df[df['sentiment_label'] == 'NEGATIVE']['text'].tolist()
        
        if len(negative_reviews) < 5:
            return [("Insufficient negative reviews", 1.0)]
        
        try:
            if self.embedding_model is None:
                raise Exception("Embedding model not available")
            
            print("Detecting complaint topics...")
            # Initialize and fit topic model
            self.topic_model = BERTopic(
                embedding_model=self.embedding_model,
                umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine'),
                nr_topics=n_topics,
                verbose=False
            )
            
            topics, _ = self.topic_model.fit_transform(negative_reviews)
            
            # Get topic info
            topic_info = self.topic_model.get_topic_info()
            
            # Format results
            complaint_topics = []
            for _, row in topic_info.iterrows():
                if row['Topic'] != -1:  # Exclude outlier topic
                    topic_words = [word for word, _ in self.topic_model.get_topic(row['Topic'])[:5]]
                    topic_label = ", ".join(topic_words[:3])
                    complaint_topics.append((topic_label, float(row['Count'])))
            
            return complaint_topics[:3]  # Return top 3
        except Exception as e:
            print(f"Using simple topic detection: {e}")
            # Simple keyword-based topic detection
            complaint_counts = {}
            for text in negative_reviews[:20]:  # Limit to first 20 for speed
                text_lower = str(text).lower()
                for category, keywords in self.financial_keywords.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            complaint_counts[category] = complaint_counts.get(category, 0) + 1
                            break
            
            # Convert to list
            complaints = [(cat.replace('_', ' ').title(), count) 
                         for cat, count in complaint_counts.items()]
            return sorted(complaints, key=lambda x: x[1], reverse=True)[:3]
    
    def analyze_product_sentiment(self, df: pd.DataFrame, product_name: str) -> SentimentResult:
        """Complete sentiment analysis for a product"""
        product_df = df[df['product'] == product_name].copy()
        
        if len(product_df) == 0:
            print(f"⚠️ No reviews found for product: {product_name}")
            # Return default result
            return SentimentResult(
                product=product_name,
                avg_sentiment=0.5,
                positive_count=0,
                negative_count=0,
                neutral_count=0,
                total_reviews=0,
                dissatisfaction_index=0,
                top_complaints=[("No data", 1.0)],
                sentiment_trend=pd.DataFrame({'date': [datetime.now()], 'sentiment_value': [0.5]}),
                risk_score=0.0
            )
        
        # Analyze sentiment
        product_df = self.batch_analyze(product_df)
        
        # Calculate metrics
        dissatisfaction_data = self.calculate_dissatisfaction_index(product_df)
        product_metrics = dissatisfaction_data.get(product_name, {})
        
        # Detect complaint topics
        complaint_topics = self.detect_complaint_topics(product_df)
        
        # Calculate sentiment trend over time
        if 'date' in product_df.columns:
            try:
                product_df['date'] = pd.to_datetime(product_df['date'])
                product_df.set_index('date', inplace=True)
                
                # Resample by month
                sentiment_trend = product_df['sentiment_value'].resample('M').mean().reset_index()
            except:
                # If date parsing fails, create simple trend
                sentiment_trend = pd.DataFrame({'date': [datetime.now()], 'sentiment_value': [product_metrics.get('avg_sentiment', 0.5)]})
        else:
            sentiment_trend = pd.DataFrame({'date': [datetime.now()], 'sentiment_value': [product_metrics.get('avg_sentiment', 0.5)]})
        
        # Calculate risk score (0-1, higher = more risky)
        risk_score = min(1.0, product_metrics.get('dissatisfaction_index', 0) / 100)
        
        return SentimentResult(
            product=product_name,
            avg_sentiment=product_metrics.get('avg_sentiment', 0.5),
            positive_count=product_metrics.get('positive_count', 0),
            negative_count=product_metrics.get('negative_count', 0),
            neutral_count=product_metrics.get('neutral_count', 0),
            total_reviews=product_metrics.get('total_reviews', 0),
            dissatisfaction_index=product_metrics.get('dissatisfaction_index', 0),
            top_complaints=complaint_topics,
            sentiment_trend=sentiment_trend,
            risk_score=risk_score
        )
    
    def create_sentiment_dashboard(self, df: pd.DataFrame, output_path: str = "reports/sentiment_dashboard.html"):
        """Create interactive sentiment dashboard"""
        # Create reports directory
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Analyze all products
        products = df['product'].unique()
        results = []
        
        print(f"\nAnalyzing {len(products)} products...")
        for product in products:
            try:
                print(f"  Processing: {product}")
                result = self.analyze_product_sentiment(df, product)
                results.append(vars(result))
            except Exception as e:
                print(f"  Error analyzing {product}: {e}")
                # Add placeholder result
                results.append({
                    'product': product,
                    'avg_sentiment': 0.5,
                    'dissatisfaction_index': 0,
                    'risk_score': 0,
                    'total_reviews': 0
                })
        
        results_df = pd.DataFrame(results)
        
        # Save results to CSV
        results_csv_path = "data/processed/sentiment_results.csv"
        os.makedirs("data/processed", exist_ok=True)
        results_df.to_csv(results_csv_path, index=False)
        print(f"\nSaved sentiment results to: {results_csv_path}")
        
        # Create simple dashboard
        try:
            print("Creating dashboard visualization...")
            fig = px.bar(
                results_df,
                x='product',
                y='dissatisfaction_index',
                title='Customer Dissatisfaction Index by Product',
                color='risk_score',
                color_continuous_scale='RdYlGn_r',
                labels={'dissatisfaction_index': 'Dissatisfaction %', 'product': 'Product'}
            )
            
            fig.update_layout(
                height=500,
                xaxis_title="Product",
                yaxis_title="Dissatisfaction Index (%)",
                showlegend=True
            )
            
            # Save dashboard
            fig.write_html(output_path)
            print(f"Dashboard saved to: {output_path}")
            
        except Exception as e:
            print(f"Warning: Could not create dashboard visualization: {e}")
            # Create simple text dashboard
            with open(output_path, 'w') as f:
                f.write("<h1>Sentiment Analysis Results</h1>")
                for _, row in results_df.iterrows():
                    f.write(f"<h3>{row['product']}</h3>")
                    f.write(f"<p>Dissatisfaction: {row['dissatisfaction_index']:.1f}%</p>")
                    f.write(f"<p>Risk Score: {row['risk_score']:.2f}</p>")
                print(f"Created simple HTML dashboard at: {output_path}")
        
        return results_df

# Test the sentiment analyzer
if __name__ == "__main__":
    print("=" * 60)
    print("SENTIMENT ANALYZER TEST")
    print("=" * 60)
    
    try:
        # Load mock data
        reviews_path = "data/mock/customer_reviews.csv"
        if os.path.exists(reviews_path):
            print(f"Loading data from: {reviews_path}")
            reviews_df = pd.read_csv(reviews_path)
            print(f"Loaded {len(reviews_df)} reviews")
        else:
            print(f"Error: Data file not found at {reviews_path}")
            print("Please run mock_data_generator.py first")
            exit(1)
        
        # Initialize analyzer
        analyzer = AdvancedSentimentAnalyzer()
        
        # Analyze sample product
        sample_product = "Alpha Growth Mutual Fund"
        print(f"\nAnalyzing sentiment for: {sample_product}")
        result = analyzer.analyze_product_sentiment(reviews_df, sample_product)
        
        print("\n" + "="*50)
        print("SENTIMENT ANALYSIS RESULTS")
        print("="*50)
        print(f"Product: {result.product}")
        print(f"Average Sentiment: {result.avg_sentiment:.2f}")
        print(f"Dissatisfaction Index: {result.dissatisfaction_index:.1f}%")
        print(f"Risk Score: {result.risk_score:.2f}")
        print(f"Total Reviews: {result.total_reviews}")
        print(f"Positive Reviews: {result.positive_count}")
        print(f"Negative Reviews: {result.negative_count}")
        print(f"Neutral Reviews: {result.neutral_count}")
        
        print("\n📢 Top Complaint Topics:")
        if result.top_complaints:
            for topic, count in result.top_complaints:
                print(f"  - {topic} ({int(count)} mentions)")
        else:
            print("  No specific complaints detected")
        
        # Create dashboard for all products
        print("\n" + "="*50)
        print("CREATING COMPREHENSIVE DASHBOARD")
        print("="*50)
        dashboard_df = analyzer.create_sentiment_dashboard(reviews_df)
        
        print("\n📊 Summary Statistics:")
        print(f"Average dissatisfaction: {dashboard_df['dissatisfaction_index'].mean():.1f}%")
        print(f"Highest risk product: {dashboard_df.loc[dashboard_df['risk_score'].idxmax(), 'product']}")
        print(f"Lowest risk product: {dashboard_df.loc[dashboard_df['risk_score'].idxmin(), 'product']}")
        
        print("\n✅ Sentiment analysis complete!")
        print(f"📁 Results saved to: data/processed/sentiment_results.csv")
        print(f"📊 Dashboard saved to: reports/sentiment_dashboard.html")
        print("\n💡 Tip: Open the HTML file in your browser to view the interactive dashboard!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()