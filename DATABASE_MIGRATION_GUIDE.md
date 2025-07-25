# Database Auto-Migration System

This document describes the database auto-migration system implemented for Sibila, which provides versioned database schema management with automated migration tracking and rollback capabilities.

## Overview

The migration system allows you to:
- Version database schema changes
- Apply migrations in order automatically  
- Track which migrations have been applied
- Rollback migrations when needed
- Maintain backward compatibility with existing code

## Architecture

### Components

1. **Migration Base Class** (`src/migrations/migration_base.py`)
   - Abstract base class for all migrations
   - Provides `up()` and `down()` methods for apply/rollback
   - Error handling and logging

2. **Migration Manager** (`src/migrations/migration_manager.py`)
   - Core migration engine
   - Tracks applied migrations in `schema_migrations` table
   - Handles migration discovery and execution
   - Provides status and rollback functionality

3. **Migration CLI** (`migrate_cli.py`)
   - Command-line interface for migration management
   - Commands: `status`, `migrate`, `rollback`, `create`

4. **Updated Migration Routine** (`src/routines/migrate.py`)
   - Enhanced with new migration system
   - Maintains backward compatibility
   - Integrates with main application startup

## Database Schema

### Migration Tracking Table

```sql
CREATE TABLE schema_migrations (
    version TEXT PRIMARY KEY,           -- Migration version (e.g., "001")
    description TEXT,                   -- Human-readable description
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checksum TEXT                       -- Reserved for future validation
);
```

### Existing Tables

The system maintains existing tables while adding versioning:

```sql
-- Document metadata
CREATE TABLE documents_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT,
    name TEXT, 
    size INTEGER,
    pages INTEGER,
    mimetype TEXT
);

-- Paragraph content with metadata
CREATE TABLE paragraphs_metadatas (
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
);
```

## Usage

### Command Line Interface

```bash
# Check migration status
python migrate_cli.py status

# Apply all pending migrations
python migrate_cli.py migrate

# Rollback the last migration
python migrate_cli.py rollback

# Create a new migration
python migrate_cli.py create "Add user authentication table"
```

### Programmatic Usage

```python
from src.routines.migrate import run_migrations, migration_status

# Apply all pending migrations
success = run_migrations()

# Get migration status
status = migration_status()
print(f"Applied: {status['total_applied']}, Pending: {status['total_pending']}")
```

### Integration with Main Application

The migration system is automatically integrated into the main application startup:

```python
# main.py
if __name__ == "__main__":
    migrate.tables()        # Legacy system (backward compatibility)
    migrate.run_migrations() # New versioned system
    app.run(...)
```

## Creating Migrations

### 1. Use CLI Tool (Recommended)

```bash
python migrate_cli.py create "Add user authentication table"
```

This creates a new migration file with the proper structure.

### 2. Manual Creation

Create a file following the naming convention: `migration_XXX_description.py`

```python
# src/migrations/migration_003_add_users_table.py

from src.migrations.migration_base import Migration

class Migration003(Migration):
    """Add users table for authentication"""
    
    def __init__(self):
        super().__init__("003", "Add users table for authentication")
    
    def up(self, conn) -> bool:
        """Apply the migration"""
        try:
            conn.execute(\"\"\"
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            \"\"\")
            
            conn.execute("CREATE INDEX idx_users_username ON users(username)")
            conn.execute("CREATE INDEX idx_users_email ON users(email)")
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration003.up(): {e}")
            return False
    
    def down(self, conn) -> bool:
        """Rollback the migration"""
        try:
            conn.execute("DROP TABLE IF EXISTS users")
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration003.down(): {e}")
            return False
```

## Migration Naming Convention

- File: `migration_XXX_description.py`
- Class: `MigrationXXX`
- Version: Zero-padded 3-digit number (001, 002, 003, etc.)
- Description: Snake_case description

Examples:
- `migration_001_initial.py` → `Migration001`
- `migration_002_add_users_table.py` → `Migration002`
- `migration_003_add_indexes.py` → `Migration003`

## Best Practices

### Migration Guidelines

1. **Always provide rollback** - Implement both `up()` and `down()` methods
2. **Test migrations** - Test both apply and rollback before deploying
3. **Keep migrations atomic** - One logical change per migration
4. **Use transactions** - Migrations should be transactional
5. **Handle errors gracefully** - Return `False` on failure

### Schema Changes

1. **Additive changes are safer** - Add tables/columns rather than modify
2. **Use IF NOT EXISTS** - For backward compatibility
3. **Create indexes separately** - Can be rolled back independently
4. **Migrate data carefully** - Consider data migration strategies

### Error Handling

```python
def up(self, conn) -> bool:
    try:
        # Migration logic here
        conn.commit()
        return True
    except Exception as e:
        print(f"Error in MigrationXXX.up(): {e}")
        # Consider conn.rollback() if needed
        return False
```

## Status and Monitoring

### Check Status

```bash
$ python migrate_cli.py status
=== Migration Status ===
Applied migrations: 1
  ✓ 001

Pending migrations: 0

✓ Database is up to date
```

### Migration Log

Applied migrations are tracked in the `schema_migrations` table:

```sql
SELECT version, description, applied_at FROM schema_migrations ORDER BY version;
```

## Rollback Strategy

### Single Migration Rollback

```bash
python migrate_cli.py rollback
```

This rolls back the last applied migration.

### Multiple Migration Rollback

For rolling back multiple migrations, use the CLI multiple times or implement programmatically:

```python
from src.migrations.migration_manager import MigrationManager

manager = MigrationManager()
applied = manager.get_applied_migrations()

# Rollback last 3 migrations
for version in reversed(applied[-3:]):
    manager.rollback_migration(version)
```

## Backward Compatibility

The system maintains full backward compatibility:

1. **Legacy `migrate.tables()`** - Still works for existing deployments
2. **Existing database schemas** - Automatically recognized
3. **No breaking changes** - Existing code continues to work

## Testing

Run the migration system tests:

```bash
python test_migration_system.py
```

This validates:
- Migration table creation
- Migration detection and loading
- Apply/rollback functionality  
- Status tracking
- Backward compatibility

## Troubleshooting

### Common Issues

1. **Migration not detected**
   - Check file naming convention
   - Ensure class name matches version
   - Verify file is in `src/migrations/`

2. **Migration fails to apply**
   - Check database connection
   - Verify SQL syntax
   - Check for existing conflicting objects

3. **Rollback fails**
   - Ensure `down()` method is implemented
   - Check for dependencies (foreign keys, etc.)
   - Verify objects exist before dropping

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Manual Recovery

If migrations get into an inconsistent state:

```sql
-- Check current state
SELECT * FROM schema_migrations;

-- Manually mark migration as applied/unapplied
INSERT INTO schema_migrations (version, description) VALUES ('XXX', 'Description');
DELETE FROM schema_migrations WHERE version = 'XXX';
```

## Future Enhancements

Potential improvements for the migration system:

1. **Checksum validation** - Detect migration file changes
2. **Parallel migrations** - Branch-aware migration handling  
3. **Data migrations** - Built-in support for data transformation
4. **Migration dependencies** - Handle complex migration dependencies
5. **Backup integration** - Automatic backup before migrations
6. **Multi-database support** - Support for multiple database engines

## Conclusion

The auto-migration system provides a robust foundation for database schema management in Sibila. It ensures consistency across environments while maintaining backward compatibility and providing tools for safe schema evolution.