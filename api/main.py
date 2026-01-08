# api/main.py - FastAPI Backend
"""
Production-ready FastAPI backend for Veritas Finance.
RESTful API for mis-selling detection system.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager, get_db
from database.schema import Alert
from backend.data_sources.api_client import DataSourceAggregator
from api.realtime import router as realtime_router
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Veritas Finance API",
    description="AI-Powered Mis-Selling Detection System API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include realtime router
app.include_router(realtime_router)

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ProductCreate(BaseModel):
    name: str
    issuer: Optional[str] = None
    category: Optional[str] = None


class PromiseData(BaseModel):
    investment_objective: Optional[str] = None
    promised_returns: Optional[str] = None
    risk_category: Optional[str] = None
    lock_in_period: Optional[str] = None
    exit_load: Optional[str] = None
    min_investment: Optional[str] = None
    key_features: Optional[List[str]] = []
    warnings: Optional[List[str]] = []
    extraction_confidence: Optional[float] = None


class ReviewData(BaseModel):
    review_text: str
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    source: str
    source_id: Optional[str] = None
    author: Optional[str] = None
    rating: Optional[int] = None


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Veritas Finance API",
        "version": "2.0.0",
        "status": "operational",
        "description": "AI-Powered Mis-Selling Detection System"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        db = DatabaseManager()
        stats = db.get_statistics()
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


@app.get("/status")
async def status():
    """System status"""
    aggregator = DataSourceAggregator()
    source_status = aggregator.get_status()
    
    db = DatabaseManager()
    stats = db.get_statistics()
    db.close()
    
    return {
        "api": "operational",
        "database": "connected",
        "data_sources": source_status,
        "statistics": stats
    }


# ============================================================================
# PRODUCT ENDPOINTS
# ============================================================================

@app.post("/api/v1/products", response_model=Dict[str, Any])
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        db = DatabaseManager()
        product_obj = db.get_or_create_product(
            name=product.name,
            issuer=product.issuer,
            category=product.category
        )
        db.close()
        
        return {
            "id": product_obj.id,
            "name": product_obj.name,
            "issuer": product_obj.issuer,
            "category": product_obj.category,
            "created_at": product_obj.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/products", response_model=List[Dict[str, Any]])
async def get_products():
    """Get all products"""
    try:
        db = DatabaseManager()
        products = db.get_all_products()
        db.close()
        
        return [
            {
                "id": p.id,
                "name": p.name,
                "issuer": p.issuer,
                "category": p.category,
                "created_at": p.created_at.isoformat()
            }
            for p in products
        ]
    except Exception as e:
        logger.error(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: int):
    """Get product by ID"""
    try:
        db = DatabaseManager()
        product = db.get_product_by_id(product_id)
        db.close()
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return {
            "id": product.id,
            "name": product.name,
            "issuer": product.issuer,
            "category": product.category
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@app.post("/api/v1/products/{product_id}/promise")
async def save_promise(product_id: int, promise: PromiseData):
    """Save promise extraction results"""
    try:
        db = DatabaseManager()
        product = db.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        promise_data = promise.dict()
        promise_obj = db.save_promise(product_id, promise_data)
        db.close()
        
        return {
            "id": promise_obj.id,
            "product_id": promise_obj.product_id,
            "promised_returns": promise_obj.promised_returns,
            "risk_category": promise_obj.risk_category,
            "extraction_confidence": promise_obj.extraction_confidence
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving promise: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/products/{product_id}/reviews")
async def save_reviews(product_id: int, reviews: List[ReviewData]):
    """Save customer reviews"""
    try:
        db = DatabaseManager()
        product = db.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        reviews_data = [r.dict() for r in reviews]
        saved_count = db.save_reviews(product_id, reviews_data)
        db.close()
        
        return {
            "product_id": product_id,
            "saved_count": saved_count,
            "total_submitted": len(reviews)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving reviews: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/products/{product_id}/risk")
async def get_risk_analysis(product_id: int):
    """Get risk analysis for a product"""
    try:
        from database.schema import GapAnalysis
        
        db = DatabaseManager()
        product = db.get_product_by_id(product_id)
        if not product:
            db.close()
            raise HTTPException(status_code=404, detail="Product not found")
        
        gap_analysis = db.session.query(GapAnalysis).filter_by(
            product_id=product_id
        ).first()
        
        if not gap_analysis:
            db.close()
            raise HTTPException(status_code=404, detail="Risk analysis not found")
        
        result = {
            "product_id": product_id,
            "product_name": product.name,
            "risk_score": gap_analysis.overall_risk_score,
            "risk_level": gap_analysis.risk_level,
            "dissatisfaction_index": gap_analysis.dissatisfaction_index,
            "mismatches": gap_analysis.mismatches,
            "recommendations": gap_analysis.recommendations,
            "last_updated": gap_analysis.last_updated.isoformat()
        }
        
        db.close()
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting risk analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DATA FETCHING ENDPOINTS
# ============================================================================

@app.post("/api/v1/products/{product_id}/fetch-data")
async def fetch_external_data(product_id: int, background_tasks: BackgroundTasks):
    """Fetch data from external sources (Twitter, Reddit, News)"""
    try:
        db = DatabaseManager()
        product = db.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Fetch data in background
        aggregator = DataSourceAggregator()
        
        def process_fetched_data():
            try:
                data = aggregator.fetch_all_sources(product.name, max_per_source=50)
                reviews = [
                    {
                        'review_text': item.get('text', ''),
                        'source': item.get('source', ''),
                        'source_id': item.get('source_id', ''),
                        'author': item.get('author', ''),
                        'review_date': item.get('review_date')
                    }
                    for item in data
                ]
                db = DatabaseManager()
                db.save_reviews(product_id, reviews)
                db.close()
            except Exception as e:
                logger.error(f"Background data fetch error: {e}")
        
        background_tasks.add_task(process_fetched_data)
        db.close()
        
        return {
            "status": "fetching",
            "product_id": product_id,
            "message": "Data fetch initiated in background"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ALERTS ENDPOINTS
# ============================================================================

@app.get("/api/v1/alerts")
async def get_alerts(limit: int = 50, status: str = "active"):
    """Get alerts"""
    try:
        db = DatabaseManager()
        if status == "active":
            alerts = db.get_active_alerts(limit)
        else:
            alerts = db.session.query(Alert).filter_by(status=status).limit(limit).all()
        db.close()
        
        return [
            {
                "id": a.id,
                "product_id": a.product_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "description": a.description,
                "status": a.status,
                "created_at": a.created_at.isoformat()
            }
            for a in alerts
        ]
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@app.get("/api/v1/statistics")
async def get_statistics():
    """Get overall statistics"""
    try:
        db = DatabaseManager()
        stats = db.get_statistics()
        db.close()
        
        return stats
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/risk/products")
async def get_high_risk_products(limit: int = 10):
    """Get high-risk products"""
    try:
        db = DatabaseManager()
        high_risk = db.get_high_risk_products(limit=limit)
        
        result = []
        for g in high_risk:
            product = db.get_product_by_id(g.product_id)
            result.append({
                "product_id": g.product_id,
                "product_name": product.name if product else "Unknown",
                "risk_score": g.overall_risk_score,
                "risk_level": g.risk_level,
                "dissatisfaction_index": g.dissatisfaction_index
            })
        
        db.close()
        return result
    except Exception as e:
        logger.error(f"Error getting high-risk products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Veritas Finance API Server Starting...")
    print("="*60)
    print("📍 API Documentation: http://localhost:8000/docs")
    print("📍 API Root: http://localhost:8000")
    print("📍 Health Check: http://localhost:8000/health")
    print("="*60 + "\n")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
