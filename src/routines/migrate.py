# flake8: noqa: E501

import logging
import traceback

from src.modules.document import document_info_repository as DocInfoRepository
from src.modules.document import paragraph_metadata_repository as ParagraphRepository
from src.migrations.migration_manager import MigrationManager

def tables():
    """Legacy table creation - kept for backward compatibility"""
    try:
        DocInfoRepository.table_documents_info()
        ParagraphRepository.table_paragraphs_metadatas()
    except Exception as e:
        logging.error(f"{e}\n{traceback.format_exc()}")

def run_migrations():
    """Run database migrations using the new versioning system"""
    try:
        manager = MigrationManager()
        success = manager.migrate()
        if success:
            logging.info("All migrations completed successfully")
        else:
            logging.error("Some migrations failed")
        return success
    except Exception as e:
        logging.error(f"Migration system error: {e}\n{traceback.format_exc()}")
        return False

def migration_status():
    """Get migration status information"""
    try:
        manager = MigrationManager()
        return manager.status()
    except Exception as e:
        logging.error(f"Failed to get migration status: {e}\n{traceback.format_exc()}")
        return {}
