# flake8: noqa: E501

import sys

from src.routines import migrate
from src.server import app


if __name__ == "__main__":
    # Run both legacy and new migration systems for compatibility
    migrate.tables()  # Legacy system for existing deployments
    migrate.run_migrations()  # New versioned migration system
    
    no_reload = '--no-reload' in sys.argv

    app.run(host="0.0.0.0", port=3000, debug=True, use_reloader=not no_reload)

