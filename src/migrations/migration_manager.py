# flake8: noqa: E501

"""
Migration manager for handling database schema versioning
"""

import os
import logging
import traceback
import importlib.util
from typing import List, Optional, Dict
from datetime import datetime

from src.modules.database import sqlitedb
from src.migrations.migration_base import Migration


class MigrationManager:
    """Manages database migrations and versioning"""
    
    def __init__(self, migrations_path: str = "src/migrations"):
        self.migrations_path = migrations_path
        self.migration_table = "schema_migrations"
    
    def ensure_migration_table(self) -> bool:
        """Create the migration tracking table if it doesn't exist"""
        try:
            conn = sqlitedb.client()
            conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.migration_table} (
                    version TEXT PRIMARY KEY,
                    description TEXT,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum TEXT
                )
            """)
            conn.commit()
            return True
        except Exception as e:
            logging.error(f"Failed to create migration table: {e}\n{traceback.format_exc()}")
            return False
    
    def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration versions"""
        try:
            conn = sqlitedb.client()
            cursor = conn.execute(f"SELECT version FROM {self.migration_table} ORDER BY version")
            return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Failed to get applied migrations: {e}\n{traceback.format_exc()}")
            return []
    
    def get_pending_migrations(self) -> List[str]:
        """Get list of pending migration files"""
        try:
            applied = set(self.get_applied_migrations())
            all_migrations = []
            
            # Look for migration files in the migrations directory
            migrations_dir = os.path.join(os.getcwd(), self.migrations_path)
            if os.path.exists(migrations_dir):
                for filename in os.listdir(migrations_dir):
                    if filename.startswith('migration_') and filename.endswith('.py') and not filename.startswith('migration_base'):
                        # Extract version from filename (e.g., migration_001_initial.py -> 001)
                        parts = filename.split('_')
                        if len(parts) >= 2:
                            version = parts[1]
                            # Only include if version is numeric and not already applied
                            if version.isdigit() and version not in applied:
                                all_migrations.append(version)
            
            return sorted(all_migrations)
        except Exception as e:
            logging.error(f"Failed to get pending migrations: {e}\n{traceback.format_exc()}")
            return []
    
    def load_migration(self, version: str) -> Optional[Migration]:
        """Load a migration class from file"""
        try:
            # Find migration file by version
            migrations_dir = os.path.join(os.getcwd(), self.migrations_path)
            migration_file = None
            
            for filename in os.listdir(migrations_dir):
                if filename.startswith(f'migration_{version}_') and filename.endswith('.py') and not filename.startswith('migration_base'):
                    migration_file = os.path.join(migrations_dir, filename)
                    break
            
            if not migration_file:
                logging.error(f"Migration file for version {version} not found")
                return None
            
            # Load the migration module
            spec = importlib.util.spec_from_file_location(f"migration_{version}", migration_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the migration class (should be named like Migration001)
            migration_class_name = f"Migration{version}"
            if hasattr(module, migration_class_name):
                return getattr(module, migration_class_name)()
            else:
                logging.error(f"Migration class {migration_class_name} not found in {migration_file}")
                return None
                
        except Exception as e:
            logging.error(f"Failed to load migration {version}: {e}\n{traceback.format_exc()}")
            return None
    
    def apply_migration(self, version: str) -> bool:
        """Apply a single migration"""
        try:
            migration = self.load_migration(version)
            if not migration:
                return False
            
            conn = sqlitedb.client()
            
            # Execute the migration
            if migration.execute(conn):
                # Record the migration as applied
                conn.execute(
                    f"INSERT INTO {self.migration_table} (version, description) VALUES (?, ?)",
                    (version, migration.description)
                )
                conn.commit()
                logging.info(f"Applied migration {version}: {migration.description}")
                return True
            else:
                logging.error(f"Failed to apply migration {version}")
                return False
                
        except Exception as e:
            logging.error(f"Error applying migration {version}: {e}\n{traceback.format_exc()}")
            return False
    
    def rollback_migration(self, version: str) -> bool:
        """Rollback a single migration"""
        try:
            migration = self.load_migration(version)
            if not migration:
                return False
            
            conn = sqlitedb.client()
            
            # Execute the rollback
            if migration.rollback(conn):
                # Remove the migration record
                conn.execute(f"DELETE FROM {self.migration_table} WHERE version = ?", (version,))
                conn.commit()
                logging.info(f"Rolled back migration {version}: {migration.description}")
                return True
            else:
                logging.error(f"Failed to rollback migration {version}")
                return False
                
        except Exception as e:
            logging.error(f"Error rolling back migration {version}: {e}\n{traceback.format_exc()}")
            return False
    
    def migrate(self) -> bool:
        """Apply all pending migrations"""
        try:
            if not self.ensure_migration_table():
                return False
            
            pending = self.get_pending_migrations()
            if not pending:
                logging.info("No pending migrations")
                return True
            
            success_count = 0
            for version in pending:
                if self.apply_migration(version):
                    success_count += 1
                else:
                    logging.error(f"Migration {version} failed, stopping migration process")
                    break
            
            logging.info(f"Applied {success_count} out of {len(pending)} migrations")
            return success_count == len(pending)
            
        except Exception as e:
            logging.error(f"Migration process failed: {e}\n{traceback.format_exc()}")
            return False
    
    def status(self) -> Dict:
        """Get migration status information"""
        try:
            self.ensure_migration_table()
            applied = self.get_applied_migrations()
            pending = self.get_pending_migrations()
            
            return {
                "applied_migrations": applied,
                "pending_migrations": pending,
                "total_applied": len(applied),
                "total_pending": len(pending)
            }
        except Exception as e:
            logging.error(f"Failed to get migration status: {e}\n{traceback.format_exc()}")
            return {
                "applied_migrations": [],
                "pending_migrations": [],
                "total_applied": 0,
                "total_pending": 0,
                "error": str(e)
            }