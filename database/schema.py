# database/schema.py - Production Database Schema
"""
PostgreSQL database schema for Veritas Finance.
Falls back to SQLite for development if PostgreSQL not available.
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Product(Base):
    """Financial product information"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    issuer = Column(String(255))
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    promises = relationship("Promise", back_populates="product", cascade="all, delete-orphan")
    sentiment_analyses = relationship("SentimentAnalysis", back_populates="product", cascade="all, delete-orphan")
    gap_analyses = relationship("GapAnalysis", back_populates="product", cascade="all, delete-orphan")


class Promise(Base):
    """Extracted promises from product documents"""
    __tablename__ = 'promises'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    
    # Extracted information
    investment_objective = Column(Text)
    promised_returns = Column(String(100))
    risk_category = Column(String(50))
    lock_in_period = Column(String(100))
    exit_load = Column(String(100))
    min_investment = Column(String(100))
    key_features = Column(JSON)  # List of features
    warnings = Column(JSON)  # List of warnings/disclaimers
    
    # Metadata
    extraction_confidence = Column(Float)
    source_document = Column(String(500))
    extraction_method = Column(String(50))  # 'nlp', 'regex', 'ml_model'
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    product = relationship("Product", back_populates="promises")


class CustomerReview(Base):
    """Customer reviews and complaints"""
    __tablename__ = 'customer_reviews'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    
    # Review content
    review_text = Column(Text, nullable=False)
    sentiment_score = Column(Float)  # -1 to 1
    sentiment_label = Column(String(20))  # 'positive', 'negative', 'neutral'
    
    # Metadata
    source = Column(String(50))  # 'twitter', 'reddit', 'playstore', 'trustpilot'
    source_id = Column(String(255))  # Original ID from source
    author = Column(String(255))
    rating = Column(Integer)  # 1-5 if available
    
    # Timestamps
    review_date = Column(DateTime)
    collected_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product")


class SentimentAnalysis(Base):
    """Aggregated sentiment analysis results"""
    __tablename__ = 'sentiment_analyses'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, unique=True)
    
    # Metrics
    avg_sentiment = Column(Float)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    total_reviews = Column(Integer, default=0)
    dissatisfaction_index = Column(Float)  # 0-100
    
    # Analysis results
    top_complaints = Column(JSON)  # List of (topic, frequency) tuples
    sentiment_trend = Column(JSON)  # Time series data
    risk_score = Column(Float)  # 0-1
    
    # Metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String(50))
    
    # Relationship
    product = relationship("Product", back_populates="sentiment_analyses")


class GapAnalysis(Base):
    """Gap analysis results - core mis-selling detection"""
    __tablename__ = 'gap_analyses'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, unique=True)
    
    # Scores
    promise_confidence = Column(Float)
    sentiment_score = Column(Float)
    dissatisfaction_index = Column(Float)
    overall_risk_score = Column(Float, index=True)  # 0-1, indexed for fast queries
    risk_level = Column(String(20), index=True)  # 'low', 'medium', 'high', 'critical'
    
    # Mismatches
    mismatches = Column(JSON)  # List of mismatch objects
    
    # Recommendations
    recommendations = Column(JSON)  # List of recommendation strings
    
    # Evidence
    evidence_sources = Column(JSON)  # List of evidence source info
    
    # Metadata
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    product = relationship("Product", back_populates="gap_analyses")


class Alert(Base):
    """Risk alerts and notifications"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    
    # Alert details
    alert_type = Column(String(50))  # 'high_risk', 'critical_risk', 'new_mismatch'
    severity = Column(String(20))  # 'low', 'medium', 'high', 'critical'
    title = Column(String(255))
    description = Column(Text)
    
    # Status
    status = Column(String(20), default='active')  # 'active', 'acknowledged', 'resolved'
    acknowledged_by = Column(String(255))
    acknowledged_at = Column(DateTime)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationship
    product = relationship("Product")


class DataSource(Base):
    """Tracks data sources and API integrations"""
    __tablename__ = 'data_sources'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)  # 'twitter', 'reddit', etc.
    source_type = Column(String(50))  # 'api', 'scraper', 'manual'
    
    # Configuration
    api_key = Column(String(500))  # Encrypted
    api_secret = Column(String(500))  # Encrypted
    is_active = Column(Boolean, default=True)
    
    # Statistics
    last_sync_at = Column(DateTime)
    total_fetched = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)


class Report(Base):
    """Generated reports"""
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    
    # Report details
    report_type = Column(String(50))  # 'executive_summary', 'full_analysis', 'evidence_package'
    title = Column(String(255))
    content = Column(Text)
    
    # File info
    file_path = Column(String(500))
    file_format = Column(String(20))  # 'pdf', 'html', 'docx'
    file_size = Column(Integer)  # bytes
    
    # Metadata
    generated_at = Column(DateTime, default=datetime.utcnow)
    generated_by = Column(String(255))
    
    # Relationship
    product = relationship("Product")


# ============================================================================
# DATABASE SETUP
# ============================================================================

def get_database_url():
    """Get database URL from environment or use SQLite fallback"""
    # Try PostgreSQL first (production)
    postgres_url = os.getenv('DATABASE_URL')
    if postgres_url:
        return postgres_url
    
    # Try individual PostgreSQL credentials
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'veritas_finance')
    
    if db_pass or db_user != 'postgres':
        return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    
    # Fallback to SQLite (development)
    return 'sqlite:///veritas_finance.db'


def create_engine_instance():
    """Create SQLAlchemy engine with proper configuration"""
    database_url = get_database_url()
    
    # SQLite specific settings
    if database_url.startswith('sqlite'):
        return create_engine(
            database_url,
            connect_args={'check_same_thread': False},
            echo=False  # Set to True for SQL query logging
        )
    
    # PostgreSQL settings
    return create_engine(
        database_url,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )


def get_session():
    """Get database session"""
    engine = create_engine_instance()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def init_database():
    """Initialize database - create all tables"""
    engine = create_engine_instance()
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    return engine


def reset_database():
    """Drop and recreate all tables (use with caution!)"""
    engine = create_engine_instance()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✅ Database reset successfully!")


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
    print("Database schema ready!")
