# database/db_manager.py - Database Manager with Helper Functions
"""
Database operations and helper functions for Veritas Finance.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json

from .schema import (
    Product, Promise, CustomerReview, SentimentAnalysis,
    GapAnalysis, Alert, DataSource, Report,
    get_session, Base
)


class DatabaseManager:
    """High-level database operations"""
    
    def __init__(self, session: Optional[Session] = None):
        self.session = session or get_session()
    
    # ========================================================================
    # PRODUCT OPERATIONS
    # ========================================================================
    
    def get_or_create_product(self, name: str, issuer: str = None, category: str = None) -> Product:
        """Get existing product or create new one"""
        product = self.session.query(Product).filter_by(name=name).first()
        if not product:
            product = Product(name=name, issuer=issuer, category=category)
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
        return product
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.session.query(Product).all()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.session.query(Product).filter_by(id=product_id).first()
    
    def get_product_by_name(self, name: str) -> Optional[Product]:
        """Get product by name"""
        return self.session.query(Product).filter_by(name=name).first()
    
    # ========================================================================
    # PROMISE OPERATIONS
    # ========================================================================
    
    def save_promise(self, product_id: int, promise_data: Dict[str, Any]) -> Promise:
        """Save or update promise for a product"""
        # Delete existing promises for this product
        self.session.query(Promise).filter_by(product_id=product_id).delete()
        
        promise = Promise(
            product_id=product_id,
            investment_objective=promise_data.get('investment_objective'),
            promised_returns=promise_data.get('promised_returns'),
            risk_category=promise_data.get('risk_category'),
            lock_in_period=promise_data.get('lock_in_period'),
            exit_load=promise_data.get('exit_load'),
            min_investment=promise_data.get('min_investment'),
            key_features=promise_data.get('key_features', []),
            warnings=promise_data.get('warnings', []),
            extraction_confidence=promise_data.get('extraction_confidence'),
            source_document=promise_data.get('source_document'),
            extraction_method=promise_data.get('extraction_method', 'ml_model')
        )
        self.session.add(promise)
        self.session.commit()
        self.session.refresh(promise)
        return promise
    
    def get_promise(self, product_id: int) -> Optional[Promise]:
        """Get promise for a product"""
        return self.session.query(Promise).filter_by(product_id=product_id).first()
    
    # ========================================================================
    # REVIEW OPERATIONS
    # ========================================================================
    
    def save_reviews(self, product_id: int, reviews: List[Dict[str, Any]]) -> int:
        """Save multiple reviews, return count saved"""
        saved = 0
        for review_data in reviews:
            # Check if review already exists
            existing = self.session.query(CustomerReview).filter_by(
                product_id=product_id,
                source=review_data.get('source'),
                source_id=review_data.get('source_id')
            ).first()
            
            if not existing:
                review = CustomerReview(
                    product_id=product_id,
                    review_text=review_data.get('review_text', ''),
                    sentiment_score=review_data.get('sentiment_score'),
                    sentiment_label=review_data.get('sentiment_label'),
                    source=review_data.get('source'),
                    source_id=review_data.get('source_id'),
                    author=review_data.get('author'),
                    rating=review_data.get('rating'),
                    review_date=review_data.get('review_date')
                )
                self.session.add(review)
                saved += 1
        
        self.session.commit()
        return saved
    
    def get_reviews(self, product_id: int, limit: int = 100) -> List[CustomerReview]:
        """Get reviews for a product"""
        return self.session.query(CustomerReview).filter_by(
            product_id=product_id
        ).order_by(desc(CustomerReview.review_date)).limit(limit).all()
    
    # ========================================================================
    # SENTIMENT ANALYSIS OPERATIONS
    # ========================================================================
    
    def save_sentiment_analysis(self, product_id: int, sentiment_data: Dict[str, Any]) -> SentimentAnalysis:
        """Save or update sentiment analysis"""
        existing = self.session.query(SentimentAnalysis).filter_by(product_id=product_id).first()
        
        if existing:
            # Update existing
            for key, value in sentiment_data.items():
                setattr(existing, key, value)
            existing.analyzed_at = datetime.utcnow()
            analysis = existing
        else:
            # Create new
            analysis = SentimentAnalysis(
                product_id=product_id,
                **sentiment_data
            )
            self.session.add(analysis)
        
        self.session.commit()
        self.session.refresh(analysis)
        return analysis
    
    def get_sentiment_analysis(self, product_id: int) -> Optional[SentimentAnalysis]:
        """Get sentiment analysis for a product"""
        return self.session.query(SentimentAnalysis).filter_by(product_id=product_id).first()
    
    # ========================================================================
    # GAP ANALYSIS OPERATIONS
    # ========================================================================
    
    def save_gap_analysis(self, product_id: int, gap_data: Dict[str, Any]) -> GapAnalysis:
        """Save or update gap analysis"""
        existing = self.session.query(GapAnalysis).filter_by(product_id=product_id).first()
        
        if existing:
            # Update existing
            for key, value in gap_data.items():
                setattr(existing, key, value)
            existing.last_updated = datetime.utcnow()
            analysis = existing
        else:
            # Create new
            analysis = GapAnalysis(
                product_id=product_id,
                **gap_data
            )
            self.session.add(analysis)
        
        self.session.commit()
        self.session.refresh(analysis)
        return analysis
    
    def get_high_risk_products(self, risk_level: str = 'high', limit: int = 10) -> List[GapAnalysis]:
        """Get products with high/critical risk"""
        return self.session.query(GapAnalysis).filter(
            GapAnalysis.risk_level.in_(['high', 'critical'])
        ).order_by(desc(GapAnalysis.overall_risk_score)).limit(limit).all()
    
    def get_all_gap_analyses(self) -> List[GapAnalysis]:
        """Get all gap analyses"""
        return self.session.query(GapAnalysis).order_by(
            desc(GapAnalysis.overall_risk_score)
        ).all()
    
    # ========================================================================
    # ALERT OPERATIONS
    # ========================================================================
    
    def create_alert(self, product_id: int, alert_data: Dict[str, Any]) -> Alert:
        """Create a new alert"""
        alert = Alert(
            product_id=product_id,
            alert_type=alert_data.get('alert_type'),
            severity=alert_data.get('severity', 'medium'),
            title=alert_data.get('title'),
            description=alert_data.get('description')
        )
        self.session.add(alert)
        self.session.commit()
        self.session.refresh(alert)
        return alert
    
    def get_active_alerts(self, limit: int = 50) -> List[Alert]:
        """Get active alerts"""
        return self.session.query(Alert).filter_by(
            status='active'
        ).order_by(desc(Alert.created_at)).limit(limit).all()
    
    # ========================================================================
    # STATISTICS & ANALYTICS
    # ========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        total_products = self.session.query(Product).count()
        total_reviews = self.session.query(CustomerReview).count()
        
        high_risk_count = self.session.query(GapAnalysis).filter(
            GapAnalysis.risk_level.in_(['high', 'critical'])
        ).count()
        
        avg_risk = self.session.query(func.avg(GapAnalysis.overall_risk_score)).scalar() or 0
        avg_dissatisfaction = self.session.query(
            func.avg(SentimentAnalysis.dissatisfaction_index)
        ).scalar() or 0
        
        active_alerts = self.session.query(Alert).filter_by(status='active').count()
        
        return {
            'total_products': total_products,
            'total_reviews': total_reviews,
            'high_risk_products': high_risk_count,
            'average_risk_score': float(avg_risk),
            'average_dissatisfaction': float(avg_dissatisfaction),
            'active_alerts': active_alerts
        }
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def close(self):
        """Close database session"""
        if self.session:
            self.session.close()


# Convenience function for quick operations
def get_db():
    """Get database manager instance"""
    return DatabaseManager()
