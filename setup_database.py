# setup_database.py - Initialize Database
"""
Setup script to initialize the database.
Run this before starting the application.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from database.schema import init_database, reset_database
from database.db_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_database(reset: bool = False):
    """Initialize or reset database"""
    try:
        if reset:
            logger.info("Resetting database...")
            reset_database()
        else:
            logger.info("Initializing database...")
            init_database()
        
        logger.info("✅ Database setup complete!")
        
        # Verify with a test query
        db = DatabaseManager()
        stats = db.get_statistics()
        logger.info(f"Database statistics: {stats}")
        db.close()
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        logger.info("💡 Tip: Make sure PostgreSQL is running, or use SQLite for development.")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Setup Veritas Finance Database')
    parser.add_argument('--reset', action='store_true', help='Reset database (drops all tables)')
    args = parser.parse_args()
    
    if args.reset:
        confirm = input("⚠️  This will DELETE ALL DATA. Continue? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            sys.exit(0)
    
    success = setup_database(reset=args.reset)
    sys.exit(0 if success else 1)
