#!/usr/bin/env python3
# flake8: noqa: E501

"""
Migration CLI tool for managing database schema versions
Usage: python migrate_cli.py [command]
Commands:
  status    - Show migration status
  migrate   - Apply all pending migrations
  rollback  - Rollback last migration
  create    - Create a new migration file
"""

import os
import sys
import argparse
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.migrations.migration_manager import MigrationManager


def cmd_status():
    """Show migration status"""
    manager = MigrationManager()
    status = manager.status()
    
    print("=== Migration Status ===")
    print(f"Applied migrations: {status['total_applied']}")
    for version in status['applied_migrations']:
        print(f"  ✓ {version}")
    
    print(f"\nPending migrations: {status['total_pending']}")
    for version in status['pending_migrations']:
        print(f"  ○ {version}")
    
    if status['total_pending'] == 0:
        print("\n✓ Database is up to date")
    else:
        print(f"\n⚠ {status['total_pending']} migrations need to be applied")


def cmd_migrate():
    """Apply all pending migrations"""
    manager = MigrationManager()
    print("=== Running Migrations ===")
    
    status = manager.status()
    pending = status['pending_migrations']
    
    if not pending:
        print("✓ No pending migrations")
        return
    
    print(f"Applying {len(pending)} migrations...")
    success = manager.migrate()
    
    if success:
        print("✓ All migrations applied successfully")
    else:
        print("✗ Some migrations failed")


def cmd_rollback():
    """Rollback the last migration"""
    manager = MigrationManager()
    applied = manager.get_applied_migrations()
    
    if not applied:
        print("No migrations to rollback")
        return
    
    last_version = applied[-1]
    print(f"Rolling back migration {last_version}...")
    
    success = manager.rollback_migration(last_version)
    if success:
        print("✓ Migration rolled back successfully")
    else:
        print("✗ Rollback failed")


def cmd_create(description):
    """Create a new migration file"""
    if not description:
        print("Error: Migration description is required")
        print("Usage: python migrate_cli.py create 'Add user table'")
        return
    
    # Get next version number
    migrations_dir = "src/migrations"
    versions = []
    
    if os.path.exists(migrations_dir):
        for filename in os.listdir(migrations_dir):
            if filename.startswith('migration_') and filename.endswith('.py'):
                try:
                    version = int(filename.split('_')[1])
                    versions.append(version)
                except ValueError:
                    continue
    
    next_version = str(max(versions) + 1).zfill(3) if versions else "001"
    
    # Create filename from description
    safe_desc = "".join(c if c.isalnum() else "_" for c in description.lower()).strip("_")
    filename = f"migration_{next_version}_{safe_desc}.py"
    filepath = os.path.join(migrations_dir, filename)
    
    # Migration template
    template = f"""# flake8: noqa: E501

\"\"\"
Migration {next_version}: {description}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
\"\"\"

from src.migrations.migration_base import Migration


class Migration{next_version}(Migration):
    \"\"\"Migration for: {description}\"\"\"
    
    def __init__(self):
        super().__init__("{next_version}", "{description}")
    
    def up(self, conn) -> bool:
        \"\"\"Apply the migration\"\"\"
        try:
            # TODO: Add your migration logic here
            # Example:
            # conn.execute(\"\"\"
            #     CREATE TABLE example (
            #         id INTEGER PRIMARY KEY,
            #         name TEXT
            #     )
            # \"\"\")
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration{next_version}.up(): {{e}}")
            return False
    
    def down(self, conn) -> bool:
        \"\"\"Rollback the migration\"\"\"
        try:
            # TODO: Add your rollback logic here
            # Example:
            # conn.execute("DROP TABLE IF EXISTS example")
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error in Migration{next_version}.down(): {{e}}")
            return False
"""
    
    try:
        with open(filepath, 'w') as f:
            f.write(template)
        print(f"✓ Created migration: {filename}")
        print(f"Edit the file to add your migration logic: {filepath}")
    except Exception as e:
        print(f"✗ Failed to create migration: {e}")


def main():
    parser = argparse.ArgumentParser(description='Database migration management tool')
    parser.add_argument('command', help='Command to run')
    parser.add_argument('description', nargs='?', help='Migration description (for create command)')
    
    args = parser.parse_args()
    
    if args.command == 'status':
        cmd_status()
    elif args.command == 'migrate':
        cmd_migrate()
    elif args.command == 'rollback':
        cmd_rollback()
    elif args.command == 'create':
        cmd_create(args.description)
    else:
        print(f"Unknown command: {args.command}")
        print("Available commands: status, migrate, rollback, create")


if __name__ == "__main__":
    main()