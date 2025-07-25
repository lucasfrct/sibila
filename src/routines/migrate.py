# flake8: noqa: E501

import logging
import traceback
import sys

# Import migration manager directly to avoid dependency issues
from src.migrations.migration_manager import MigrationManager

# Try to import legacy repositories with fallback
try:
    from src.modules.document import document_info_repository as DocInfoRepository
    from src.modules.document import paragraph_metadata_repository as ParagraphRepository
    LEGACY_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Legacy repository modules not available: {e}")
    DocInfoRepository = None
    ParagraphRepository = None
    LEGACY_AVAILABLE = False

def tables():
    """Legacy table creation - kept for backward compatibility"""
    if not LEGACY_AVAILABLE:
        logging.warning("Legacy table creation skipped - dependencies not available")
        return
        
    try:
        logging.info("Running legacy table creation for backward compatibility...")
        DocInfoRepository.table_documents_info()
        ParagraphRepository.table_paragraphs_metadatas()
        logging.info("Legacy tables created successfully")
    except Exception as e:
        logging.error(f"Legacy table creation failed: {e}\n{traceback.format_exc()}")

def run_migrations():
    """Run database migrations using the new versioning system"""
    try:
        logging.info("Starting auto-migration system...")
        manager = MigrationManager()
        
        # Get current status
        status = manager.status()
        total_pending = status.get('total_pending', 0)
        total_applied = status.get('total_applied', 0)
        
        logging.info(f"Migration status: {total_applied} applied, {total_pending} pending")
        
        if total_pending == 0:
            logging.info("Database is up to date - no migrations needed")
            return True
        
        logging.info(f"Applying {total_pending} pending migrations...")
        success = manager.migrate()
        
        if success:
            logging.info(f"Auto-migration completed successfully - applied {total_pending} migrations")
        else:
            logging.error("Some migrations failed during auto-migration")
            
        return success
        
    except Exception as e:
        logging.error(f"Auto-migration system error: {e}\n{traceback.format_exc()}")
        return False

def auto_migrate_on_startup():
    """
    Comprehensive auto-migration that runs on application startup.
    This ensures the database is properly initialized and up to date.
    """
    try:
        logging.info("=== Starting Auto-Migration on Startup ===")
        
        # Step 1: Run legacy table creation for backward compatibility (if available)
        if LEGACY_AVAILABLE:
            logging.info("Step 1: Running legacy table creation...")
            tables()
        else:
            logging.info("Step 1: Skipping legacy table creation (dependencies not available)")
        
        # Step 2: Run the new versioned migration system
        logging.info("Step 2: Running versioned migration system...")
        migration_success = run_migrations()
        
        if migration_success:
            logging.info("✓ Auto-migration completed successfully")
            
            # Step 3: Show final status
            status = migration_status()
            if status:
                logging.info(f"✓ Database status: {status.get('total_applied', 0)} migrations applied")
                if status.get('database_ready', False):
                    logging.info("✓ Database is ready for use")
                
        else:
            logging.warning("⚠ Some migrations failed, but application will continue")
            
        logging.info("=== Auto-Migration Startup Complete ===")
        return migration_success
        
    except Exception as e:
        logging.error(f"Critical error in auto-migration startup: {e}\n{traceback.format_exc()}")
        logging.warning("⚠ Auto-migration failed, but application will continue")
        return False

def migration_status():
    """Get migration status information"""
    try:
        manager = MigrationManager()
        return manager.status()
    except Exception as e:
        logging.error(f"Failed to get migration status: {e}\n{traceback.format_exc()}")
        return {}

def check_database_health():
    """Check if the database is accessible and has the required structure"""
    try:
        from src.modules.database import sqlitedb
        
        conn = sqlitedb.client()
        if conn is None:
            logging.error("Database connection failed")
            return False
            
        # Test basic connectivity
        cursor = conn.execute("SELECT 1")
        cursor.fetchone()
        
        logging.info("✓ Database connectivity test passed")
        return True
        
    except Exception as e:
        logging.error(f"Database health check failed: {e}\n{traceback.format_exc()}")
        return False
