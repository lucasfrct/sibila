# flake8: noqa: E501

"""
Base migration class for database schema versioning
"""

import logging
import traceback
from abc import ABC, abstractmethod
from typing import Optional

from src.modules.database import sqlitedb


class Migration(ABC):
    """Base class for database migrations"""
    
    def __init__(self, version: str, description: str):
        self.version = version
        self.description = description
    
    @abstractmethod
    def up(self, conn) -> bool:
        """Apply the migration (upgrade)"""
        pass
    
    @abstractmethod
    def down(self, conn) -> bool:
        """Rollback the migration (downgrade)"""
        pass
    
    def execute(self, conn) -> bool:
        """Execute the migration with error handling"""
        try:
            return self.up(conn)
        except Exception as e:
            logging.error(f"Migration {self.version} failed: {e}\n{traceback.format_exc()}")
            return False
    
    def rollback(self, conn) -> bool:
        """Rollback the migration with error handling"""
        try:
            return self.down(conn)
        except Exception as e:
            logging.error(f"Migration {self.version} rollback failed: {e}\n{traceback.format_exc()}")
            return False