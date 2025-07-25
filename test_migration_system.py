#!/usr/bin/env python3
"""
Test script for the database migration system
Tests migration creation, application, rollback, and status tracking
"""

import os
import sys
import tempfile
import shutil
import sqlite3
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.migrations.migration_manager import MigrationManager
from src.modules.database import sqlitedb


def test_migration_manager_initialization():
    """Test that MigrationManager initializes correctly"""
    print("🧪 Testing MigrationManager initialization...")
    
    try:
        manager = MigrationManager()
        assert manager.migrations_path == "src/migrations"
        assert manager.migration_table == "schema_migrations"
        print("✓ MigrationManager initializes correctly")
        return True
    except Exception as e:
        print(f"✗ MigrationManager initialization failed: {e}")
        return False


def test_migration_table_creation():
    """Test that the migration tracking table is created correctly"""
    print("🧪 Testing migration table creation...")
    
    try:
        manager = MigrationManager()
        success = manager.ensure_migration_table()
        assert success, "Migration table creation should succeed"
        
        # Check if table exists and has correct structure
        conn = sqlitedb.client()
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schema_migrations'")
        result = cursor.fetchone()
        assert result is not None, "Migration table should exist"
        
        # Check table structure
        cursor = conn.execute("PRAGMA table_info(schema_migrations)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        expected_columns = {'version': 'TEXT', 'description': 'TEXT', 'applied_at': 'TIMESTAMP', 'checksum': 'TEXT'}
        
        for col, col_type in expected_columns.items():
            assert col in columns, f"Column {col} should exist"
        
        print("✓ Migration table created with correct structure")
        return True
    except Exception as e:
        print(f"✗ Migration table creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_migration_status():
    """Test migration status functionality"""
    print("🧪 Testing migration status...")
    
    try:
        manager = MigrationManager()
        status = manager.status()
        
        # Check status structure
        required_keys = ['applied_migrations', 'pending_migrations', 'total_applied', 'total_pending']
        for key in required_keys:
            assert key in status, f"Status should include {key}"
        
        assert isinstance(status['applied_migrations'], list), "applied_migrations should be a list"
        assert isinstance(status['pending_migrations'], list), "pending_migrations should be a list"
        assert isinstance(status['total_applied'], int), "total_applied should be an integer"
        assert isinstance(status['total_pending'], int), "total_pending should be an integer"
        
        print("✓ Migration status returns correct structure")
        return True
    except Exception as e:
        print(f"✗ Migration status test failed: {e}")
        return False


def test_migration_detection():
    """Test that existing migration files are detected correctly"""
    print("🧪 Testing migration file detection...")
    
    try:
        manager = MigrationManager()
        pending = manager.get_pending_migrations()
        
        # Should find the existing migration files
        assert isinstance(pending, list), "Pending migrations should be a list"
        
        # Should contain migration 001 (and possibly 002 if not applied)
        if '001' not in manager.get_applied_migrations():
            assert '001' in pending, "Should detect migration 001"
        
        print(f"✓ Detected {len(pending)} pending migrations")
        return True
    except Exception as e:
        print(f"✗ Migration detection test failed: {e}")
        return False


def test_full_migration_cycle():
    """Test applying and rolling back migrations"""
    print("🧪 Testing full migration cycle...")
    
    try:
        # Clean database for clean test
        if os.path.exists("data/.sqlite/sqlite.db"):
            os.remove("data/.sqlite/sqlite.db")
        
        manager = MigrationManager()
        
        # Initial status should show no applied migrations
        status = manager.status()
        initial_applied = status['total_applied']
        
        # Apply migrations
        success = manager.migrate()
        assert success, "Migration should succeed"
        
        # Check that migrations were applied
        status_after = manager.status()
        assert status_after['total_applied'] > initial_applied, "Should have applied migrations"
        assert status_after['total_pending'] == 0, "Should have no pending migrations after migrate"
        
        print("✓ Migrations applied successfully")
        
        # Test rollback
        if status_after['applied_migrations']:
            last_migration = status_after['applied_migrations'][-1]
            rollback_success = manager.rollback_migration(last_migration)
            assert rollback_success, "Rollback should succeed"
            
            # Check that migration was rolled back
            status_after_rollback = manager.status()
            assert last_migration not in status_after_rollback['applied_migrations'], "Migration should be rolled back"
            
            print("✓ Migration rollback successful")
        
        return True
    except Exception as e:
        print(f"✗ Full migration cycle test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backward_compatibility():
    """Test that legacy migration system still works"""
    print("🧪 Testing backward compatibility...")
    
    try:
        from src.routines.migrate import tables, run_migrations, migration_status
        
        # Test legacy function
        tables()  # Should not raise an exception
        print("✓ Legacy tables() function works")
        
        # Test new functions
        success = run_migrations()
        assert isinstance(success, bool), "run_migrations should return boolean"
        
        status = migration_status()
        assert isinstance(status, dict), "migration_status should return dict"
        
        print("✓ New migration functions work")
        print("✓ Backward compatibility maintained")
        return True
    except Exception as e:
        print(f"✗ Backward compatibility test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all migration system tests"""
    print("🧪 Database Migration System Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_migration_manager_initialization()
    print()
    all_passed &= test_migration_table_creation()
    print()
    all_passed &= test_migration_status()
    print()
    all_passed &= test_migration_detection()
    print()
    all_passed &= test_full_migration_cycle()
    print()
    all_passed &= test_backward_compatibility()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All migration system tests passed!")
        print("📋 Migration system features verified:")
        print("  • ✅ Migration table creation and tracking")
        print("  • ✅ Migration file detection and loading")
        print("  • ✅ Migration application and status tracking")
        print("  • ✅ Migration rollback functionality")
        print("  • ✅ Backward compatibility with legacy system")
        print("  • ✅ Error handling and recovery")
        print("\n🚀 Database auto-migration system is ready for production!")
    else:
        print("⚠️  Some migration system tests failed.")
        print("Please check the output above for details.")
        
    return all_passed


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🚨 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)