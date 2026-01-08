# backend/realtime/scheduler.py - Scheduled Jobs for Automated Analysis
"""
Scheduled job system for automated analysis and monitoring.
"""

import asyncio
from datetime import datetime, timedelta
import logging
from typing import Callable, Optional

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    from apscheduler.triggers.interval import IntervalTrigger
    APSCHEDULER_AVAILABLE = True
except ImportError:
    APSCHEDULER_AVAILABLE = False
    # Fallback - simple scheduler
    class AsyncIOScheduler:
        def __init__(self): pass
        def start(self): pass
        def shutdown(self): pass
        def add_job(self, *args, **kwargs): pass
    class CronTrigger:
        def __init__(self, **kwargs): pass
    class IntervalTrigger:
        def __init__(self, **kwargs): pass

logger = logging.getLogger(__name__)


class JobScheduler:
    """Scheduled job manager for automated tasks"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.running = False
    
    def start(self):
        """Start the scheduler"""
        if not self.running:
            self.scheduler.start()
            self.running = True
            logger.info("✅ Job scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
            logger.info("Job scheduler stopped")
    
    def add_daily_analysis_job(self, func: Callable, hour: int = 2, minute: int = 0):
        """Schedule daily analysis job"""
        self.scheduler.add_job(
            func,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_analysis',
            name='Daily Product Analysis',
            replace_existing=True
        )
        logger.info(f"✅ Daily analysis scheduled for {hour:02d}:{minute:02d}")
    
    def add_hourly_data_fetch(self, func: Callable):
        """Schedule hourly data fetching"""
        self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(hours=1),
            id='hourly_data_fetch',
            name='Hourly Data Fetch',
            replace_existing=True
        )
        logger.info("✅ Hourly data fetch scheduled")
    
    def add_realtime_monitoring(self, func: Callable, interval_minutes: int = 5):
        """Schedule real-time monitoring"""
        self.scheduler.add_job(
            func,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id='realtime_monitoring',
            name='Real-time Monitoring',
            replace_existing=True
        )
        logger.info(f"✅ Real-time monitoring scheduled (every {interval_minutes} minutes)")


# Global scheduler instance
scheduler = JobScheduler()


async def run_daily_analysis():
    """Run daily analysis pipeline"""
    try:
        logger.info("🔄 Starting scheduled daily analysis...")
        from main_pipeline_upgraded import VeritasFinancePipelineUpgraded
        
        pipeline = VeritasFinancePipelineUpgraded(
            use_database=True,
            use_real_apis=True
        )
        success = pipeline.run_pipeline()
        
        if success:
            logger.info("✅ Daily analysis completed successfully")
        else:
            logger.error("❌ Daily analysis failed")
            
    except Exception as e:
        logger.error(f"❌ Scheduled analysis error: {e}")


async def run_hourly_data_fetch():
    """Fetch new data from APIs hourly"""
    try:
        logger.info("🔄 Fetching new data from APIs...")
        from database.db_manager import DatabaseManager
        from backend.data_sources.api_client import DataSourceAggregator
        
        db = DatabaseManager()
        aggregator = DataSourceAggregator()
        
        # Get all products
        products = db.get_all_products()
        
        for product in products:
            try:
                data = aggregator.fetch_all_sources(product.name, max_per_source=20)
                
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
                
                saved = db.save_reviews(product.id, reviews)
                logger.info(f"  ✅ {product.name}: Saved {saved} new reviews")
                
            except Exception as e:
                logger.error(f"  ⚠️ Error fetching data for {product.name}: {e}")
        
        db.close()
        logger.info("✅ Hourly data fetch completed")
        
    except Exception as e:
        logger.error(f"❌ Hourly data fetch error: {e}")


async def run_realtime_monitoring():
    """Real-time monitoring - check for new high-risk products"""
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        high_risk = db.get_high_risk_products(limit=10)
        
        # Check for new critical alerts
        new_alerts = []
        for gap in high_risk:
            product = db.get_product_by_id(gap.product_id)
            if product and gap.risk_level == 'critical':
                # Check if alert already exists
                existing_alerts = db.session.query(db.__class__.__module__.Alert).filter_by(
                    product_id=gap.product_id,
                    status='active'
                ).count()
                
                if existing_alerts == 0:
                    alert = db.create_alert(gap.product_id, {
                        'alert_type': 'critical_risk',
                        'severity': 'critical',
                        'title': f"CRITICAL: {product.name}",
                        'description': f"Risk score: {gap.overall_risk_score:.2f}"
                    })
                    new_alerts.append({
                        'product': product.name,
                        'risk_score': gap.overall_risk_score
                    })
        
        db.close()
        
        if new_alerts:
            logger.warning(f"⚠️ {len(new_alerts)} new critical alerts detected!")
            # Broadcast alerts via WebSocket
            from backend.realtime.websocket_server import broadcast_alert
            for alert in new_alerts:
                await broadcast_alert(alert)
        
    except Exception as e:
        logger.error(f"❌ Real-time monitoring error: {e}")


def initialize_scheduler():
    """Initialize and start scheduled jobs"""
    scheduler.start()
    
    # Schedule daily analysis at 2 AM
    scheduler.add_daily_analysis_job(run_daily_analysis, hour=2, minute=0)
    
    # Schedule hourly data fetch
    scheduler.add_hourly_data_fetch(run_hourly_data_fetch)
    
    # Schedule real-time monitoring every 5 minutes
    scheduler.add_realtime_monitoring(run_realtime_monitoring, interval_minutes=5)
    
    logger.info("✅ All scheduled jobs initialized")
