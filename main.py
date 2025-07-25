# flake8: noqa: E501

import sys
import logging

from src.routines import migrate
from src.server import app

# Configure logging for startup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

if __name__ == "__main__":
    logging.info("🚀 Starting Sibila Application...")
    
    # Check database health before migration
    if not migrate.check_database_health():
        logging.warning("⚠ Database health check failed, but proceeding with startup...")
    
    # Run comprehensive auto-migration on startup
    migrate.auto_migrate_on_startup()
    
    # Parse command line arguments
    no_reload = '--no-reload' in sys.argv
    
    logging.info("🌐 Starting Flask server...")
    logging.info("📍 Server will be available at: http://0.0.0.0:3000")
    
    try:
        app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=not no_reload)
    except KeyboardInterrupt:
        logging.info("👋 Server stopped by user")
    except Exception as e:
        logging.error(f"💥 Server startup failed: {e}")
        sys.exit(1)

