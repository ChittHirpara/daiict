# mock_data_generator.py - FIXED VERSION
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from faker import Faker
import random
from pathlib import Path
import os
import warnings
warnings.filterwarnings('ignore')

# Initialize Faker
fake = Faker()

class FinancialDataGenerator:
    def __init__(self):
        self.products = [
            "Alpha Growth Mutual Fund",
            "SecureLife Insurance Policy", 
            "MaxReturns Fixed Deposit",
            "WealthBuilder Pension Plan",
            "EasyInvest Savings Account"
        ]
        self.banks = ["HDFC", "ICICI", "SBI", "Axis", "Kotak"]
        self.complaint_types = [
            "hidden charges", "poor returns", "bad service",
            "misleading information", "difficult claims",
            "long processing time", "agent misconduct"
        ]
    
    def generate_product_document(self, product_name):
        """Generate a realistic product PDF content (simulated)"""
        doc = {
            "product_name": product_name,
            "issuer": random.choice(self.banks),
            "launch_date": str(fake.date_between(start_date='-2y', end_date='today')),  # Convert to string
            "investment_objective": random.choice([
                "To generate capital appreciation by investing in equity and equity-related instruments",
                "To provide income distribution and capital appreciation", 
                "Capital protection with moderate returns",
                "High growth through aggressive equity allocation"
            ]),
            "promised_returns": f"{random.uniform(8, 15):.1f}% p.a.",
            "risk_category": random.choice(["Low", "Moderate", "High"]),
            "lock_in_period": f"{random.choice([1, 3, 5, 10])} years",
            "exit_load": f"{random.uniform(0.5, 2):.1f}% if redeemed before {random.choice([1, 3])} years",
            "min_investment": f"₹{random.choice([1000, 5000, 10000, 50000])}",
            "key_features": [
                "Monthly income option available",
                "Tax benefits under section 80C", 
                "Life cover included",
                "Loan against policy available"
            ],
            "warnings": [
                "Returns are not guaranteed",
                "Past performance is not indicative of future results",
                "Market risks apply"
            ]
        }
        
        # Save as JSON (simulating PDF content extraction)
        # Use os.makedirs which handles existing folders better
        os.makedirs("data/mock/product_docs", exist_ok=True)
        file_path = Path(f"data/mock/product_docs/{product_name.replace(' ', '_')}.json")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(doc, f, indent=2, default=str)
        
        return doc
    
    def generate_customer_reviews(self, num_reviews=200):  # Reduced for testing
        """Generate realistic customer reviews/social media posts"""
        reviews = []
        
        for i in range(num_reviews):
            product = random.choice(self.products)
            bank = random.choice(self.banks)
            date = fake.date_between(start_date='-1y', end_date='today')
            
            # Create different types of reviews
            review_type = random.choices(
                ['positive', 'negative', 'neutral'],
                weights=[0.3, 0.5, 0.2]
            )[0]
            
            complaint = random.choice(self.complaint_types) if review_type == 'negative' else None
            
            if review_type == 'positive':
                templates = [
                    f"Happy with my {product} from {bank}. Returns are as promised.",
                    f"{bank}'s {product} gave me good returns this quarter.",
                    f"No complaints about {product}. Service was excellent."
                ]
                sentiment_score = random.uniform(0.7, 1.0)
            elif review_type == 'negative':
                templates = [
                    f"Avoid {product} from {bank}! They have {complaint}.",
                    f"Terrible experience with {product}. {complaint.replace('_', ' ').title()}.",
                    f"{bank} misled me about {product}. Now facing {complaint}."
                ]
                sentiment_score = random.uniform(0.0, 0.3)
            else:
                templates = [
                    f"Mixed feelings about {product}. Some good, some bad.",
                    f"{product} from {bank} is okay. Nothing special.",
                    f"Not sure about {product}. Need to wait and watch."
                ]
                sentiment_score = random.uniform(0.3, 0.7)
            
            review = {
                "review_id": f"rev_{i:04d}",  # Simplified ID
                "product": product,
                "bank": bank,
                "date": str(date),  # Convert to string
                "text": random.choice(templates),
                "source": random.choice(["Twitter", "Reddit", "Play Store", "Trustpilot"]),
                "rating": random.randint(1, 5),
                "verified_purchase": random.choice([True, False]),
                "location": fake.city(),
                "sentiment_score": sentiment_score,
                "complaint_type": complaint
            }
            reviews.append(review)
        
        # Save to CSV
        os.makedirs("data/mock", exist_ok=True)
        df = pd.DataFrame(reviews)
        df.to_csv("data/mock/customer_reviews.csv", index=False)
        return df
    
    def generate_time_series_data(self):
        """Generate time-series sentiment data"""
        dates = pd.date_range(start='2023-01-01', end='2023-03-31', freq='D')  # Reduced timeframe
        data = []
        
        for product in self.products:
            base_sentiment = random.uniform(0.3, 0.7)
            for date in dates:
                # Add some randomness
                noise = random.uniform(-0.2, 0.2)
                sentiment = max(0, min(1, base_sentiment + noise))
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'product': product,
                    'sentiment': sentiment,
                    'volume': random.randint(5, 50)
                })
        
        df = pd.DataFrame(data)
        df.to_csv("data/mock/sentiment_time_series.csv", index=False)
    
    def generate_all_data(self):
        """Generate all mock data"""
        print("Generating product documents...")
        product_docs = []
        for product in self.products:
            doc = self.generate_product_document(product)
            product_docs.append(doc)
        
        print("Generating customer reviews...")
        reviews_df = self.generate_customer_reviews(200)  # Smaller dataset
        
        print("Generating time-series data...")
        self.generate_time_series_data()
        
        print("\n✅ Data generation complete!")
        return product_docs, reviews_df

# Run data generation
if __name__ == "__main__":
    generator = FinancialDataGenerator()
    product_docs, reviews_df = generator.generate_all_data()
    print(f"✓ Generated {len(product_docs)} product documents in: data/mock/product_docs/")
    print(f"✓ Generated {len(reviews_df)} customer reviews in: data/mock/customer_reviews.csv")
    print(f"✓ Generated time-series data in: data/mock/sentiment_time_series.csv")
    
    # Show sample of what was created
    print("\n📊 Sample Product Document:")
    print(json.dumps(product_docs[0], indent=2))
    
    print("\n📊 Sample Customer Review:")
    print(reviews_df.iloc[0].to_dict())