# flake8: noqa: E501

"""
Migration 001: Initial schema
Creates the initial database tables for documents and paragraphs
"""

from src.migrations.migration_base import Migration


class Migration001(Migration):
    """Initial schema migration"""
    
    def __init__(self):
        super().__init__("001", "Initial schema: create documents_info and paragraphs_metadatas tables")
    
    def up(self, conn) -> bool:
        """Create initial tables"""
        try:
            # Create documents_info table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS documents_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT,
                    name TEXT,
                    size INTEGER,
                    pages INTEGER,
                    mimetype TEXT
                )
            """)
            
            # Create paragraphs_metadatas table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS paragraphs_metadatas (
                    uuid TEXT PRIMARY KEY,
                    path TEXT,
                    page INTEGER,
                    name TEXT,
                    source TEXT,
                    letters INTEGER,
                    content TEXT,
                    
                    distance REAL,
                    mimetype TEXT,
                    size INTEGER,

                    phrases INTEGER,
                    lines INTEGER,
                    chunks INTEGER
                )
            """)
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration001.up(): {e}")
            return False
    
    def down(self, conn) -> bool:
        """Drop initial tables"""
        try:
            conn.execute("DROP TABLE IF EXISTS paragraphs_metadatas")
            conn.execute("DROP TABLE IF EXISTS documents_info")
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration001.down(): {e}")
            return False