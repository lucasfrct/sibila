# flake8: noqa: E501

"""
Migration 001: Initial schema
Creates the initial database tables for documents and paragraphs
This migration ensures the core schema exists and handles existing tables gracefully.
"""

from src.migrations.migration_base import Migration


class Migration001(Migration):
    """Initial schema migration"""
    
    def __init__(self):
        super().__init__("001", "Initial schema: create documents_info and paragraphs_metadatas tables")
    
    def up(self, conn) -> bool:
        """Create initial tables - handles existing tables gracefully"""
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
            
            # Create helpful indexes for better performance
            try:
                conn.execute("CREATE INDEX IF NOT EXISTS idx_documents_path ON documents_info(path)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_paragraphs_path ON paragraphs_metadatas(path)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_paragraphs_page ON paragraphs_metadatas(page)")
            except Exception as idx_error:
                # Index creation failure shouldn't fail the migration
                print(f"Warning: Some indexes could not be created: {idx_error}")
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration001.up(): {e}")
            return False
    
    def down(self, conn) -> bool:
        """Drop initial tables - with safety checks"""
        try:
            # Check if tables exist before dropping
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('paragraphs_metadatas', 'documents_info')
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            if 'paragraphs_metadatas' in existing_tables:
                conn.execute("DROP TABLE paragraphs_metadatas")
                
            if 'documents_info' in existing_tables:
                conn.execute("DROP TABLE documents_info")
                
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration001.down(): {e}")
            return False